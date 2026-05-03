//! OxiEML CLI — Parse, evaluate, and generate EML expressions.
//!
//! Usage:
//!   oxieml "E(1, 1)"                     # Evaluate EML expression
//!   oxieml -g pi                          # Generate EML for π
//!   oxieml -g "sin(x0)" x0=0.5           # Generate & evaluate sin
//!   oxieml --file expression.txt          # Read from file
//!   echo "E(1, 1)" | oxieml              # Read from stdin
//!   oxieml --lower "E(x0,1)" --format latex   # Print LaTeX lowered form
//!   oxieml --lower "E(x0,1)" --format json    # Print JSON lowered form

use oxieml::canonical::Canonical;
use oxieml::eval::EvalCtx;
use oxieml::parser::{parse, to_compact_string};
use oxieml::tree::EmlTree;
use std::io::IsTerminal;
use std::io::Read;

/// Known mathematical constants to check against.
const KNOWN_CONSTANTS: &[(&str, f64)] = &[
    ("e (Euler's number)", std::f64::consts::E),
    ("pi", std::f64::consts::PI),
    ("tau (2*pi)", std::f64::consts::TAU),
    ("ln(2)", std::f64::consts::LN_2),
    ("ln(10)", std::f64::consts::LN_10),
    ("sqrt(2)", std::f64::consts::SQRT_2),
    ("1/sqrt(2)", std::f64::consts::FRAC_1_SQRT_2),
    ("1/pi", std::f64::consts::FRAC_1_PI),
    ("2/pi", std::f64::consts::FRAC_2_PI),
    ("2/sqrt(pi)", std::f64::consts::FRAC_2_SQRT_PI),
    ("pi/2", std::f64::consts::FRAC_PI_2),
    ("pi/3", std::f64::consts::FRAC_PI_3),
    ("pi/4", std::f64::consts::FRAC_PI_4),
    ("pi/6", std::f64::consts::FRAC_PI_6),
    ("pi/8", std::f64::consts::FRAC_PI_8),
    ("log2(e)", std::f64::consts::LOG2_E),
    ("log10(e)", std::f64::consts::LOG10_E),
    ("golden ratio (phi)", 1.618_033_988_749_895),
    ("0", 0.0),
    ("1", 1.0),
    ("2", 2.0),
    ("3", 3.0),
    ("-1", -1.0),
];

// ================================================================
// Output format
// ================================================================

/// Selects the output representation for results.
#[derive(Debug, Clone, PartialEq, Eq)]
enum OutputFormat {
    /// Human-readable mathematical notation (default).
    Pretty,
    /// LaTeX math-mode expression.
    Latex,
    /// Hand-rolled JSON with a stable `version:1` envelope.
    Json,
}

impl OutputFormat {
    /// Parse `--format <value>` from the argument list.
    ///
    /// Returns `Ok(Pretty)` when the flag is absent (default).
    fn from_args(args: &[String]) -> Result<Self, String> {
        let Some(pos) = args.iter().position(|a| a == "--format") else {
            return Ok(Self::Pretty);
        };
        let val = args
            .get(pos + 1)
            .ok_or_else(|| "--format requires a value: pretty, latex, or json".to_string())?;
        match val.as_str() {
            "pretty" => Ok(Self::Pretty),
            "latex" => Ok(Self::Latex),
            "json" => Ok(Self::Json),
            other => Err(format!(
                "--format: unknown value '{other}'; expected pretty, latex, or json"
            )),
        }
    }
}

/// Parse `--output <path>` from the argument list.
///
/// Returns `Ok(None)` when the flag is absent (stdout).
fn output_path(args: &[String]) -> Result<Option<std::path::PathBuf>, String> {
    let Some(pos) = args.iter().position(|a| a == "--output") else {
        return Ok(None);
    };
    let val = args
        .get(pos + 1)
        .ok_or_else(|| "--output requires a file path".to_string())?;
    Ok(Some(std::path::PathBuf::from(val)))
}

/// Write `content` to `path` when `Some`, or to stdout when `None`.
fn write_output(
    content: &str,
    path: &Option<std::path::PathBuf>,
) -> Result<(), Box<dyn std::error::Error>> {
    match path {
        None => {
            print!("{content}");
            Ok(())
        }
        Some(p) => std::fs::write(p, content).map_err(Into::into),
    }
}

// ================================================================
// main
// ================================================================

fn main() {
    let args: Vec<String> = std::env::args().collect();

    // --help / -h
    if args.iter().any(|a| a == "--help" || a == "-h") {
        print_help();
        return;
    }

    // --version / -V
    if args.iter().any(|a| a == "--version" || a == "-V") {
        println!("oxieml {}", env!("CARGO_PKG_VERSION"));
        return;
    }

    // --format / --output are global flags consumed by subcommands.
    let fmt = match OutputFormat::from_args(&args) {
        Ok(f) => f,
        Err(e) => {
            eprintln!("Error: {e}");
            std::process::exit(1);
        }
    };
    let out = match output_path(&args) {
        Ok(p) => p,
        Err(e) => {
            eprintln!("Error: {e}");
            std::process::exit(1);
        }
    };

    // --lower flag: lower an EML expression and format the result
    if let Some(pos) = args.iter().position(|a| a == "--lower") {
        let expr_str = match args.get(pos + 1) {
            Some(s) => s.clone(),
            None => {
                eprintln!("Error: --lower requires an expression argument");
                print_usage();
                std::process::exit(1);
            }
        };
        if let Err(e) = run_lower(&expr_str, &fmt, &out) {
            eprintln!("Error: {e}");
            std::process::exit(1);
        }
        return;
    }

    // Check for --gen / -g flag (generate mode)
    if let Some(pos) = args.iter().position(|a| a == "--gen" || a == "-g") {
        let expr = args.get(pos + 1).unwrap_or_else(|| {
            eprintln!("Error: --gen requires a function/constant name");
            print_usage();
            std::process::exit(1);
        });
        let vars = parse_var_assignments(&args);
        run_generate(expr, &vars);
        return;
    }

    // Check for --grad / -d flag (symbolic gradient)
    if let Some(pos) = args.iter().position(|a| a == "--grad" || a == "-d") {
        let wrt_str = match args.get(pos + 1) {
            Some(s) => s,
            None => {
                eprintln!("Error: --grad requires a variable index (e.g., --grad 0)");
                print_usage();
                std::process::exit(1);
            }
        };
        let wrt = match wrt_str.parse::<usize>() {
            Ok(n) => n,
            Err(_) => {
                eprintln!(
                    "Error: --grad requires a non-negative integer variable index, got '{wrt_str}'"
                );
                std::process::exit(1);
            }
        };
        let expr = match args.get(pos + 2) {
            Some(s) => s.clone(),
            None => {
                eprintln!("Error: --grad <idx> requires an expression argument");
                print_usage();
                std::process::exit(1);
            }
        };
        let vars = parse_var_assignments(&args);
        run_grad(&expr, wrt, &vars);
        return;
    }

    // Check for --list / -l flag (list all known functions)
    if args.iter().any(|a| a == "--list" || a == "-l") {
        print_known_functions();
        return;
    }

    // Check for --symreg / -s flag (symbolic regression)
    if args.iter().any(|a| a == "--symreg" || a == "-s") {
        if let Err(e) = run_symreg(&args, &fmt, &out) {
            eprintln!("Error: {e}");
            std::process::exit(1);
        }
        return;
    }

    let input = match get_input(&args) {
        Ok(s) => s,
        Err(e) => {
            eprintln!("Error: {e}");
            print_usage();
            std::process::exit(1);
        }
    };

    let input = input.trim();
    if input.is_empty() {
        eprintln!("Error: empty input");
        print_usage();
        std::process::exit(1);
    }

    // Try EML parse first; if it fails, try as a generate request
    match parse(input) {
        Ok(tree) => {
            let vars = parse_var_assignments(&args);
            if let Err(e) = run_evaluate_fmt(&tree, input, &vars, &fmt, &out) {
                eprintln!("Error: {e}");
                std::process::exit(1);
            }
        }
        Err(parse_err) => {
            // Maybe the user typed a function name like "pi" or "sin(x0)"
            let vars = parse_var_assignments(&args);
            if try_generate(input).is_some() {
                run_generate(input, &vars);
            } else {
                eprintln!("Parse error: {parse_err}");
                eprintln!();
                eprintln!("Hint: Use -g to generate EML from a function name:");
                eprintln!("  oxieml -g pi");
                eprintln!("  oxieml -g \"sin(x0)\"");
                std::process::exit(1);
            }
        }
    }
}

// ================================================================
// --lower subcommand: lower an EML expression and format
// ================================================================

fn run_lower(
    expr_str: &str,
    fmt: &OutputFormat,
    out: &Option<std::path::PathBuf>,
) -> Result<(), Box<dyn std::error::Error>> {
    let tree = parse(expr_str).map_err(|e| format!("parse error: {e}"))?;
    let lowered = tree.lower().simplify();
    let pretty = lowered.to_pretty();
    let latex = lowered.to_latex();

    let content = match fmt {
        OutputFormat::Pretty => format!("{pretty}\n"),
        OutputFormat::Latex => format!("$${latex}$$\n"),
        OutputFormat::Json => {
            // Hand-rolled JSON — no serde dependency.
            let pretty_escaped = json_escape_str(&pretty);
            let latex_escaped = json_escape_str(&latex);
            format!(
                "{{\"version\":1,\"formulas\":[{{\"pretty\":\"{pretty_escaped}\",\"latex\":\"{latex_escaped}\"}}]}}\n"
            )
        }
    };

    write_output(&content, out)
}

// ================================================================
// Generate mode: function/constant name → EML expression
// ================================================================

fn run_generate(expr: &str, vars: &[f64]) {
    let tree = match try_generate(expr) {
        Some(t) => t,
        None => {
            eprintln!("Unknown function or constant: \"{expr}\"");
            eprintln!();
            eprintln!("Use --list to see all available functions.");
            std::process::exit(1);
        }
    };

    let compact = to_compact_string(&tree);

    println!("=== OxiEML Generator ===\n");
    println!("Function: {expr}");
    println!("Depth:    {}", tree.depth());
    println!("Size:     {} nodes", tree.size());
    println!();
    println!("EML expression:");
    println!("{compact}");
    println!();

    // Also show the eml(...) notation
    let display = format!("{tree}");
    if display.len() <= 500 {
        println!("eml notation:");
        println!("{display}");
        println!();
    }

    // Evaluate if no variables or variables are provided
    let num_vars = count_variables(&tree);
    if num_vars == 0 {
        // Constant — evaluate directly
        let ctx = EvalCtx::new(&[]);
        println!("--- Evaluation ---");
        match tree.eval_real(&ctx) {
            Ok(val) => {
                println!("  Result: {val}");
                println!("  Result (full precision): {val:.17e}");
                println!();
                check_known_constants(val);
            }
            Err(_) => {
                // Try complex
                match tree.eval_complex(&[]) {
                    Ok(z) => {
                        println!("  Complex result: {} + {}i", z.re, z.im);
                        if z.im.abs() > 1e-10 {
                            check_known_constants_labeled("  Im", z.im);
                        }
                        if z.re.abs() > 1e-10 {
                            check_known_constants_labeled("  Re", z.re);
                        }
                    }
                    Err(e) => println!("  Evaluation failed: {e}"),
                }
            }
        }
    } else if !vars.is_empty() {
        // Variables provided — evaluate
        let ctx = EvalCtx::new(vars);
        println!("--- Evaluation ---");
        print!("  Variables: ");
        for (i, v) in vars.iter().enumerate() {
            if i > 0 {
                print!(", ");
            }
            print!("x{i} = {v}");
        }
        println!();
        match tree.eval_real(&ctx) {
            Ok(val) => {
                println!("  Result: {val}");
                println!("  Result (full precision): {val:.17e}");
                println!();
                check_known_constants(val);
            }
            Err(e) => println!("  Evaluation failed: {e}"),
        }
    } else {
        println!("(Provide variable values to evaluate, e.g., x0=1.5)");
    }
}

/// Try to parse a function/constant name and build the corresponding EML tree.
fn try_generate(expr: &str) -> Option<EmlTree> {
    let expr = expr.trim();

    // Constants (no arguments)
    match expr {
        "pi" | "π" => return Some(Canonical::pi()),
        "e" | "euler" => return Some(Canonical::euler()),
        "0" | "zero" => return Some(Canonical::zero()),
        "i" | "imag" => return Some(Canonical::imag_unit()),
        "-1" | "neg_one" => return Some(Canonical::neg_one()),
        "-2" | "neg_two" => return Some(Canonical::neg_two()),
        _ => {}
    }

    // nat(N) — natural number
    if let Some(inner) = strip_func(expr, "nat") {
        if let Ok(n) = inner.parse::<u64>() {
            if n >= 1 {
                return Some(Canonical::nat(n));
            }
        }
        return None;
    }

    // Unary functions: func(arg)
    // First try to extract (func_name, arg_string)
    if let Some((func, arg_str)) = parse_func_call(expr) {
        let arg = parse_arg(arg_str)?;
        return match func {
            "exp" => Some(Canonical::exp(&arg)),
            "ln" | "log" => Some(Canonical::ln(&arg)),
            "neg" => Some(Canonical::neg(&arg)),
            "sin" => Some(Canonical::sin(&arg)),
            "cos" => Some(Canonical::cos(&arg)),
            "tan" => Some(Canonical::tan(&arg)),
            "arcsin" | "asin" => Some(Canonical::arcsin(&arg)),
            "arccos" | "acos" => Some(Canonical::arccos(&arg)),
            "arctan" | "atan" => Some(Canonical::arctan(&arg)),
            "sinh" => Some(Canonical::sinh(&arg)),
            "cosh" => Some(Canonical::cosh(&arg)),
            "tanh" => Some(Canonical::tanh(&arg)),
            "arcsinh" | "asinh" => Some(Canonical::arcsinh(&arg)),
            "arccosh" | "acosh" => Some(Canonical::arccosh(&arg)),
            "arctanh" | "atanh" => Some(Canonical::arctanh(&arg)),
            "sqrt" | "√" => Some(Canonical::sqrt(&arg)),
            "abs" => Some(Canonical::abs(&arg)),
            "square" => Some(Canonical::square(&arg)),
            "reciprocal" | "inv" => Some(Canonical::reciprocal(&arg)),
            _ => None,
        };
    }

    // Bare function name → default to x0 as argument
    let x0 = EmlTree::var(0);
    match expr {
        "exp" => Some(Canonical::exp(&x0)),
        "ln" | "log" => Some(Canonical::ln(&x0)),
        "neg" => Some(Canonical::neg(&x0)),
        "sin" => Some(Canonical::sin(&x0)),
        "cos" => Some(Canonical::cos(&x0)),
        "tan" => Some(Canonical::tan(&x0)),
        "arcsin" | "asin" => Some(Canonical::arcsin(&x0)),
        "arccos" | "acos" => Some(Canonical::arccos(&x0)),
        "arctan" | "atan" => Some(Canonical::arctan(&x0)),
        "sinh" => Some(Canonical::sinh(&x0)),
        "cosh" => Some(Canonical::cosh(&x0)),
        "tanh" => Some(Canonical::tanh(&x0)),
        "arcsinh" | "asinh" => Some(Canonical::arcsinh(&x0)),
        "arccosh" | "acosh" => Some(Canonical::arccosh(&x0)),
        "arctanh" | "atanh" => Some(Canonical::arctanh(&x0)),
        "sqrt" => Some(Canonical::sqrt(&x0)),
        "abs" => Some(Canonical::abs(&x0)),
        "square" => Some(Canonical::square(&x0)),
        "reciprocal" | "inv" => Some(Canonical::reciprocal(&x0)),
        _ => {
            // Try binary: "add", "sub", etc. with default x0, x1
            let x1 = EmlTree::var(1);
            match expr {
                "add" => Some(Canonical::add(&x0, &x1)),
                "sub" => Some(Canonical::sub(&x0, &x1)),
                "mul" => Some(Canonical::mul(&x0, &x1)),
                "div" => Some(Canonical::div(&x0, &x1)),
                "pow" => Some(Canonical::pow(&x0, &x1)),
                _ => None,
            }
        }
    }
}

/// Parse "func(args)" → ("func", "args")
fn parse_func_call(expr: &str) -> Option<(&str, &str)> {
    let open = expr.find('(')?;
    if !expr.ends_with(')') {
        return None;
    }
    let func = expr[..open].trim();
    let inner = &expr[open + 1..expr.len() - 1];
    Some((func, inner.trim()))
}

/// Parse a function argument: "x0", "x1", "1", "e", "pi", or nested function
fn parse_arg(s: &str) -> Option<EmlTree> {
    let s = s.trim();

    // Variable: x0, x1, ...
    if let Some(idx_str) = s.strip_prefix('x') {
        if let Ok(idx) = idx_str.parse::<usize>() {
            return Some(EmlTree::var(idx));
        }
    }

    // Constant
    match s {
        "1" => return Some(EmlTree::one()),
        "e" | "euler" => return Some(Canonical::euler()),
        "pi" | "π" => return Some(Canonical::pi()),
        "0" | "zero" => return Some(Canonical::zero()),
        _ => {}
    }

    // Number literal
    if let Ok(n) = s.parse::<u64>() {
        if n >= 1 {
            return Some(Canonical::nat(n));
        }
    }

    // Nested function call
    if let Some((func, inner)) = parse_func_call(s) {
        let inner_arg = parse_arg(inner)?;
        return match func {
            "exp" => Some(Canonical::exp(&inner_arg)),
            "ln" | "log" => Some(Canonical::ln(&inner_arg)),
            "neg" => Some(Canonical::neg(&inner_arg)),
            "sin" => Some(Canonical::sin(&inner_arg)),
            "cos" => Some(Canonical::cos(&inner_arg)),
            "tan" => Some(Canonical::tan(&inner_arg)),
            "sqrt" => Some(Canonical::sqrt(&inner_arg)),
            "square" => Some(Canonical::square(&inner_arg)),
            _ => None,
        };
    }

    None
}

/// Extract inner string from "func(inner)"
fn strip_func<'a>(expr: &'a str, func: &str) -> Option<&'a str> {
    let rest = expr.strip_prefix(func)?;
    let rest = rest.strip_prefix('(')?;
    let rest = rest.strip_suffix(')')?;
    Some(rest.trim())
}

fn print_known_functions() {
    println!("=== Available Functions & Constants ===\n");
    println!("Constants:");
    println!("  pi, π          iπ (use in trig constructions)");
    println!("  e, euler       Euler's number (2.71828...)");
    println!("  0, zero        Zero = ln(1)");
    println!("  -1, neg_one    Negative one");
    println!("  -2, neg_two    Negative two");
    println!("  i, imag        Imaginary unit = exp(iπ/2)");
    println!("  nat(N)         Natural number N (1, 2, 3, ...)");
    println!();
    println!("Unary functions (default arg: x0):");
    println!("  exp             exp(x) = eml(x, 1)");
    println!("  ln, log         ln(x)");
    println!("  neg             -x");
    println!("  sqrt            √x");
    println!("  square          x²");
    println!("  abs             |x|");
    println!("  reciprocal, inv 1/x");
    println!();
    println!("Trigonometric:");
    println!("  sin, cos, tan");
    println!("  arcsin/asin, arccos/acos, arctan/atan");
    println!();
    println!("Hyperbolic:");
    println!("  sinh, cosh, tanh");
    println!("  arcsinh/asinh, arccosh/acosh, arctanh/atanh");
    println!();
    println!("Binary functions (default args: x0, x1):");
    println!("  add             x + y");
    println!("  sub             x - y");
    println!("  mul             x * y");
    println!("  div             x / y");
    println!("  pow             x ^ y");
    println!();
    println!("Examples:");
    println!("  oxieml -g pi");
    println!("  oxieml -g e");
    println!("  oxieml -g sin             # sin(x0) template");
    println!("  oxieml -g \"sin(x0)\" x0=0.5");
    println!("  oxieml -g \"exp(x0)\" x0=1.0");
    println!("  oxieml -g \"sqrt(x0)\" x0=4.0");
    println!("  oxieml -g nat(5)");
}

// ================================================================
// Evaluate mode: EML expression → result (with format support)
// ================================================================

fn run_evaluate_fmt(
    tree: &EmlTree,
    input: &str,
    vars: &[f64],
    fmt: &OutputFormat,
    out: &Option<std::path::PathBuf>,
) -> Result<(), Box<dyn std::error::Error>> {
    let lowered = tree.lower().simplify();
    let pretty = lowered.to_pretty();
    let latex = lowered.to_latex();

    let content = match fmt {
        OutputFormat::Pretty => {
            // Classic verbose output piped to a single string.
            let mut buf = String::new();
            buf.push_str("=== OxiEML Expression Evaluator ===\n\n");

            if input.len() > 200 {
                buf.push_str(&format!(
                    "Input: {}... ({} chars)\n\n",
                    &input[..200],
                    input.len()
                ));
            } else {
                buf.push_str(&format!("Input: {input}\n\n"));
            }

            buf.push_str("--- Tree Statistics ---\n");
            buf.push_str(&format!("  Depth: {}\n", tree.depth()));
            buf.push_str(&format!("  Size (nodes): {}\n", tree.size()));
            buf.push_str(&format!("  Variables used: {}\n\n", count_variables(tree)));

            let compact = to_compact_string(tree);
            if compact.len() <= 200 {
                buf.push_str(&format!("Compact: {compact}\n\n"));
            }

            let ctx = EvalCtx::new(vars);
            buf.push_str("--- Real Evaluation ---\n");
            if !vars.is_empty() {
                buf.push_str("  Variables: ");
                for (i, v) in vars.iter().enumerate() {
                    if i > 0 {
                        buf.push_str(", ");
                    }
                    buf.push_str(&format!("x{i} = {v}"));
                }
                buf.push('\n');
            }
            match tree.eval_real(&ctx) {
                Ok(val) => {
                    buf.push_str(&format!("  Result: {val}\n"));
                    buf.push_str(&format!("  Result (full precision): {val:.17e}\n\n"));
                }
                Err(e) => {
                    buf.push_str(&format!("  Real evaluation failed: {e}\n\n"));
                }
            }

            buf.push_str("--- Lowered Form ---\n");
            if pretty.len() <= 500 {
                buf.push_str(&format!("  {pretty}\n\n"));
            } else {
                buf.push_str(&format!(
                    "  (expression too large to display, {} chars)\n\n",
                    pretty.len()
                ));
            }

            buf.push_str("--- Lowered Evaluation ---\n");
            let lowered_val = lowered.eval(vars);
            buf.push_str(&format!("  Result: {lowered_val}\n"));
            buf.push_str(&format!("  Result (full precision): {lowered_val:.17e}\n"));
            buf
        }
        OutputFormat::Latex => {
            format!("$${latex}$$\n")
        }
        OutputFormat::Json => {
            let val = lowered.eval(vars);
            let pretty_escaped = json_escape_str(&pretty);
            let latex_escaped = json_escape_str(&latex);
            format!(
                "{{\"version\":1,\"result\":{val},\"pretty\":\"{pretty_escaped}\",\"latex\":\"{latex_escaped}\"}}\n"
            )
        }
    };

    write_output(&content, out)
}

// ================================================================
// Grad mode: symbolic partial derivative of an EML expression
// ================================================================

fn run_grad(expr: &str, wrt: usize, vars: &[f64]) {
    let tree = match parse(expr) {
        Ok(t) => t,
        Err(e) => {
            eprintln!("Parse error: {e}");
            std::process::exit(1);
        }
    };
    let lowered = tree.lower().simplify();
    let grad = lowered.grad(wrt);
    println!("Expression:    {lowered}");
    println!("d/dx{wrt}:         {grad}");

    // Optional numerical evaluation at provided variable bindings.
    if !vars.is_empty() {
        let ops = grad.to_oxiblas_ops();
        let result = oxieml::LoweredOp::eval_ops(&ops, vars);
        print!("At [");
        for (i, v) in vars.iter().enumerate() {
            if i > 0 {
                print!(", ");
            }
            print!("x{i}={v}");
        }
        println!("]:   {result}");
    }
}

// ================================================================
// Symreg mode: discover closed-form formulas from tabular data
// ================================================================

fn run_symreg(
    args: &[String],
    fmt: &OutputFormat,
    out: &Option<std::path::PathBuf>,
) -> Result<(), Box<dyn std::error::Error>> {
    use oxieml::symreg::{SymRegConfig, SymRegEngine};

    // Required: --vars N
    let num_vars = parse_named_usize(args, "--vars")?
        .ok_or_else(|| "--symreg requires --vars <N> (N >= 1)".to_string())?;
    if num_vars == 0 {
        return Err("--vars must be at least 1".into());
    }

    // Optional: --top K
    let top_k = parse_named_usize(args, "--top")?.unwrap_or(3);
    if top_k == 0 {
        return Err("--top must be at least 1".into());
    }

    // Build SymRegConfig, forwarding optional flags.
    let mut config = SymRegConfig::default();
    if let Some(v) = parse_named_usize(args, "--max-depth")? {
        config.max_depth = v;
    }
    if let Some(v) = parse_named_usize(args, "--max-iter")? {
        config.max_iter = v;
    }
    if let Some(v) = parse_named_f64(args, "--learning-rate")? {
        config.learning_rate = v;
    }
    if let Some(v) = parse_named_f64(args, "--tolerance")? {
        config.tolerance = v;
    }
    if let Some(v) = parse_named_f64(args, "--complexity-penalty")? {
        config.complexity_penalty = v;
    }
    if let Some(v) = parse_named_usize(args, "--num-restarts")? {
        config.num_restarts = v;
    }

    // Optional: --strategy exhaustive | beam:<N>
    if let Some(pos) = args.iter().position(|a| a == "--strategy") {
        let val = args
            .get(pos + 1)
            .ok_or("--strategy requires a value: exhaustive or beam:<N>")?;
        config.strategy = parse_strategy(val)?;
    }

    // Read dataset text from --file or stdin.
    let text = get_symreg_data(args)?;
    let (inputs, targets) = parse_dataset(&text, num_vars)?;
    if inputs.is_empty() {
        return Err("no data: dataset is empty".into());
    }

    let engine = SymRegEngine::new(config);
    let formulas = engine
        .discover(&inputs, &targets, num_vars)
        .map_err(|e| format!("symreg failed: {e}"))?;

    if formulas.is_empty() {
        return Err("no formulas discovered".into());
    }

    let limit = top_k.min(formulas.len());

    let content = format_symreg_results(&formulas[..limit], fmt);
    write_output(&content, out)
}

/// Format the top-K discovered formulas according to the requested output format.
fn format_symreg_results(formulas: &[oxieml::DiscoveredFormula], fmt: &OutputFormat) -> String {
    match fmt {
        OutputFormat::Pretty => {
            let mut buf = String::new();
            for (i, f) in formulas.iter().enumerate() {
                buf.push_str(&format!(
                    "Rank {}: {}   mse={:.4}   complexity={}   score={:.4}\n",
                    i + 1,
                    f.pretty,
                    f.mse,
                    f.complexity,
                    f.score
                ));
            }
            buf
        }
        OutputFormat::Latex => {
            let mut buf = String::new();
            for (i, f) in formulas.iter().enumerate() {
                let latex = f.to_latex();
                buf.push_str(&format!(
                    "Rank {}: $${}$$   mse={:.4}   complexity={}\n",
                    i + 1,
                    latex,
                    f.mse,
                    f.complexity
                ));
            }
            buf
        }
        OutputFormat::Json => {
            // Hand-rolled JSON — no serde.
            let mut buf = String::new();
            buf.push_str("{\"version\":1,\"formulas\":[");
            for (i, f) in formulas.iter().enumerate() {
                if i > 0 {
                    buf.push(',');
                }
                let pretty_escaped = json_escape_str(&f.pretty);
                let latex = f.to_latex();
                let latex_escaped = json_escape_str(&latex);
                buf.push_str(&format!(
                    "{{\"rank\":{rank},\"mse\":{mse},\"complexity\":{complexity},\"score\":{score},\"pretty\":\"{pretty_escaped}\",\"latex\":\"{latex_escaped}\"}}",
                    rank = i + 1,
                    mse = f.mse,
                    complexity = f.complexity,
                    score = f.score,
                ));
            }
            buf.push_str("]}\n");
            buf
        }
    }
}

/// Escape a string for embedding in a JSON string literal.
///
/// Handles the characters that are mandatory escapes per RFC 8259:
/// `"`, `\`, and the control characters U+0000–U+001F.
fn json_escape_str(s: &str) -> String {
    let mut out = String::with_capacity(s.len());
    for ch in s.chars() {
        match ch {
            '"' => out.push_str("\\\""),
            '\\' => out.push_str("\\\\"),
            '\n' => out.push_str("\\n"),
            '\r' => out.push_str("\\r"),
            '\t' => out.push_str("\\t"),
            c if (c as u32) < 0x20 => {
                out.push_str(&format!("\\u{:04x}", c as u32));
            }
            c => out.push(c),
        }
    }
    out
}

/// Parse whitespace-separated numeric dataset text.
///
/// - Lines starting with `#` or blank lines are skipped.
/// - Every other line must contain exactly `num_vars + 1` f64 values.
/// - First `num_vars` values become the input row; the last is the target.
fn parse_dataset(text: &str, num_vars: usize) -> Result<(Vec<Vec<f64>>, Vec<f64>), String> {
    let mut inputs: Vec<Vec<f64>> = Vec::new();
    let mut targets: Vec<f64> = Vec::new();
    let expected = num_vars + 1;

    for (lineno, raw) in text.lines().enumerate() {
        let line = raw.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        let values: Vec<f64> = line
            .split_whitespace()
            .map(|tok| {
                tok.parse::<f64>()
                    .map_err(|_| format!("line {}: invalid number '{}'", lineno + 1, tok))
            })
            .collect::<Result<Vec<f64>, String>>()?;
        if values.len() != expected {
            return Err(format!(
                "line {}: expected {} floats ({} vars + 1 target), got {}",
                lineno + 1,
                expected,
                num_vars,
                values.len()
            ));
        }
        let target = values[num_vars];
        let row: Vec<f64> = values[..num_vars].to_vec();
        inputs.push(row);
        targets.push(target);
    }

    Ok((inputs, targets))
}

/// Read symreg dataset text from `--file <path>` or stdin (no positional fallback).
fn get_symreg_data(args: &[String]) -> Result<String, String> {
    if let Some(pos) = args.iter().position(|a| a == "--file" || a == "-f") {
        let path = args.get(pos + 1).ok_or("--file requires a path argument")?;
        return std::fs::read_to_string(path)
            .map_err(|e| format!("failed to read file '{path}': {e}"));
    }

    if std::io::stdin().is_terminal() {
        return Err("no data: provide a dataset via --file <path> or stdin".to_string());
    }

    let mut buf = String::new();
    std::io::stdin()
        .read_to_string(&mut buf)
        .map_err(|e| format!("failed to read stdin: {e}"))?;
    Ok(buf)
}

/// Look up `--name <value>` and parse as `usize`. Returns `None` if the flag is absent.
fn parse_named_usize(args: &[String], name: &str) -> Result<Option<usize>, String> {
    let Some(pos) = args.iter().position(|a| a == name) else {
        return Ok(None);
    };
    let val = args
        .get(pos + 1)
        .ok_or_else(|| format!("{name} requires a value"))?;
    val.parse::<usize>()
        .map(Some)
        .map_err(|_| format!("{name}: expected non-negative integer, got '{val}'"))
}

/// Parse `--strategy` value: `"exhaustive"` or `"beam:<N>"`.
fn parse_strategy(val: &str) -> Result<oxieml::symreg::SymRegStrategy, String> {
    use oxieml::symreg::SymRegStrategy;
    if val == "exhaustive" {
        return Ok(SymRegStrategy::Exhaustive);
    }
    if let Some(n_str) = val.strip_prefix("beam:") {
        let width = n_str.parse::<usize>().map_err(|_| {
            format!("--strategy beam:<N>: expected positive integer, got '{n_str}'")
        })?;
        if width == 0 {
            return Err("--strategy beam:<N>: N must be at least 1".to_string());
        }
        return Ok(SymRegStrategy::Beam { width });
    }
    Err(format!(
        "--strategy: unknown value '{val}'; expected 'exhaustive' or 'beam:<N>' (e.g. beam:10)"
    ))
}

/// Look up `--name <value>` and parse as `f64`. Returns `None` if the flag is absent.
fn parse_named_f64(args: &[String], name: &str) -> Result<Option<f64>, String> {
    let Some(pos) = args.iter().position(|a| a == name) else {
        return Ok(None);
    };
    let val = args
        .get(pos + 1)
        .ok_or_else(|| format!("{name} requires a value"))?;
    val.parse::<f64>()
        .map(Some)
        .map_err(|_| format!("{name}: expected floating-point number, got '{val}'"))
}

// ================================================================
// Input handling
// ================================================================

fn get_input(args: &[String]) -> Result<String, String> {
    if let Some(pos) = args.iter().position(|a| a == "--file" || a == "-f") {
        let path = args.get(pos + 1).ok_or("--file requires a path argument")?;
        return std::fs::read_to_string(path)
            .map_err(|e| format!("failed to read file '{path}': {e}"));
    }

    for arg in args.iter().skip(1) {
        if !arg.contains('=') && !arg.starts_with('-') {
            return Ok(arg.clone());
        }
    }

    if std::io::stdin().is_terminal() {
        return Err("no expression provided".to_string());
    }

    let mut buf = String::new();
    std::io::stdin()
        .read_to_string(&mut buf)
        .map_err(|e| format!("failed to read stdin: {e}"))?;
    Ok(buf)
}

fn parse_var_assignments(args: &[String]) -> Vec<f64> {
    let mut vars: Vec<(usize, f64)> = Vec::new();

    for arg in args.iter().skip(1) {
        if let Some(eq_pos) = arg.find('=') {
            let name = &arg[..eq_pos];
            let val_str = &arg[eq_pos + 1..];
            if let Some(idx_str) = name.strip_prefix('x') {
                if let (Ok(idx), Ok(val)) = (idx_str.parse::<usize>(), val_str.parse::<f64>()) {
                    vars.push((idx, val));
                }
            }
        }
    }

    if vars.is_empty() {
        return Vec::new();
    }

    let max_idx = vars.iter().map(|(i, _)| *i).max().unwrap_or(0);
    let mut result = vec![0.0; max_idx + 1];
    for (idx, val) in vars {
        result[idx] = val;
    }
    result
}

fn count_variables(tree: &oxieml::EmlTree) -> usize {
    let mut max_var: Option<usize> = None;
    for node in tree.iter_postorder() {
        if let oxieml::EmlNode::Var(idx) = node {
            match max_var {
                None => max_var = Some(*idx),
                Some(m) if *idx > m => max_var = Some(*idx),
                _ => {}
            }
        }
    }
    match max_var {
        None => 0,
        Some(m) => m + 1,
    }
}

fn check_known_constants(val: f64) {
    println!("  --- Constant matching ---");
    let mut found = false;

    for &(name, constant) in KNOWN_CONSTANTS {
        let diff = (val - constant).abs();
        if diff < 1e-10 {
            println!("  MATCH: {name} = {constant}");
            println!("         difference = {diff:.2e}");
            found = true;
        } else if diff < 1e-4 {
            println!("  CLOSE: {name} = {constant}");
            println!("         difference = {diff:.2e}");
            found = true;
        }
    }

    for &(name, constant) in KNOWN_CONSTANTS {
        if constant == 0.0 {
            continue;
        }
        let diff = (val - (-constant)).abs();
        if diff < 1e-10 {
            println!("  MATCH: -{name} = {}", -constant);
            println!("         difference = {diff:.2e}");
            found = true;
        }
    }

    for n in 2..=10 {
        let n_f = n as f64;
        let diff = (val - n_f).abs();
        if diff < 1e-10 {
            println!("  MATCH: {n}");
            println!("         difference = {diff:.2e}");
            found = true;
        }
    }

    if !found {
        println!("  No known constant matches found.");
    }
}

fn check_known_constants_labeled(label: &str, val: f64) {
    for &(name, constant) in KNOWN_CONSTANTS {
        let diff = (val - constant).abs();
        if diff < 1e-4 {
            let quality = if diff < 1e-10 { "MATCH" } else { "CLOSE" };
            println!("  {quality}: {label} ~ {name} (diff = {diff:.2e})");
        }
        if constant != 0.0 {
            let diff_neg = (val - (-constant)).abs();
            if diff_neg < 1e-4 {
                let quality = if diff_neg < 1e-10 { "MATCH" } else { "CLOSE" };
                println!("  {quality}: {label} ~ -{name} (diff = {diff_neg:.2e})");
            }
        }
    }
}

fn usage_text() -> &'static str {
    concat!(
        "\n",
        "Usage:\n",
        "  oxieml \"E(1, 1)\"                     # Evaluate EML expression\n",
        "  oxieml \"E(x0, 1)\" x0=2.0             # With variable bindings\n",
        "  oxieml -g pi                           # Generate EML for π\n",
        "  oxieml -g sin                          # Generate EML for sin(x0)\n",
        "  oxieml -g \"sin(x0)\" x0=0.5            # Generate & evaluate\n",
        "  oxieml --lower \"E(x0,1)\"              # Lower & print expression\n",
        "  oxieml --lower \"E(x0,1)\" --format latex  # LaTeX output\n",
        "  oxieml --lower \"E(x0,1)\" --format json   # JSON output\n",
        "  oxieml --grad 0 \"E(x0, 1)\"            # Symbolic derivative of exp(x0)\n",
        "  oxieml -d 0 \"E(x0, 1)\" x0=2.0         # Derivative + numerical value\n",
        "  oxieml -l                              # List all functions\n",
        "  oxieml --help                          # Show this help\n",
        "  oxieml --version                       # Show version\n",
        "  oxieml --file expression.txt           # Read from file\n",
        "  echo \"E(1, 1)\" | oxieml               # Read from stdin\n",
        "  oxieml --symreg --vars 1 --file data.txt  # Discover formula from data\n",
        "\n",
        "Flags:\n",
        "  --gen  <name>, -g <name>    Generate EML tree for a named function/constant\n",
        "  --lower <expr>              Lower & simplify an EML expression\n",
        "  --grad <idx>,  -d <idx>     Compute symbolic partial derivative w.r.t. variable <idx>\n",
        "                              of the given expression (via lowered IR + simplify)\n",
        "  --list, -l                  List all available functions/constants\n",
        "  --file <path>, -f <path>    Read expression (or dataset, with --symreg) from file\n",
        "  --help, -h                  Show this help\n",
        "  --version, -V               Show version\n",
        "\n",
        "Output flags (apply to --lower, --symreg, and default eval mode):\n",
        "  --format <fmt>              Output format: pretty (default), latex, json\n",
        "  --output <path>             Write output to file instead of stdout\n",
        "\n",
        "Symbolic regression (--symreg / -s):\n",
        "  Discover closed-form formulas from tabular data. Data is read from\n",
        "  --file <path> or stdin. Lines starting with '#' and blank lines are\n",
        "  skipped. Each remaining line must contain exactly <vars>+1 whitespace-\n",
        "  separated f64 values: x0 x1 ... x(N-1) target.\n",
        "\n",
        "  --symreg, -s                Enable symbolic regression mode\n",
        "  --vars <N>                  (required) Number of input variables per row\n",
        "  --top <K>                   Number of formulas to print (default 3)\n",
        "\n",
        "  Forwarding flags (all optional, fall back to SymRegConfig::default()):\n",
        "  --max-depth <usize>         Maximum tree depth to explore\n",
        "  --max-iter <usize>          Maximum optimization iterations per topology\n",
        "  --learning-rate <f64>       Adam learning rate\n",
        "  --tolerance <f64>           Convergence tolerance (MSE)\n",
        "  --complexity-penalty <f64>  Occam's razor coefficient\n",
        "  --num-restarts <usize>      Random restarts per topology\n",
        "  --strategy <s>              Search strategy: exhaustive (default) or beam:<N>\n",
        "                              e.g. --strategy beam:20 keeps top 20 candidates\n",
        "\n",
        "Notation:\n",
        "  1         The constant 1\n",
        "  x0, x1    Variables\n",
        "  E(a, b)   The EML operator: exp(a) - ln(b)\n",
        "  eml(a, b) Alternative notation for E(a, b)",
    )
}

fn print_usage() {
    eprintln!("{}", usage_text());
}

fn print_help() {
    println!("{}", usage_text());
}

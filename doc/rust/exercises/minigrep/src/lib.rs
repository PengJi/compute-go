use std::error::Error;
use std::env;
use std::fs;

pub struct Config {
    pub query: String,
    pub filename: String,
    pub case_sensitive: bool,
}

impl Config {
    pub fn new(args: &[String]) -> Result<Config, &'static str> {
        if args.len() < 3 {
            return Err("not enough arguments");
        }

        let query = args[1].clone();
        let filename = args[2].clone();
        // 使用 Result 的 is_err 方法来检查其是否是一个 error（也就是环境变量未被设置的情况）
        let case_sensitive = env::var("CASE_SENSITIVE").is_err();

        Ok(Config {
            query,
            filename,
            case_sensitive,
        })
    }
}

// 定义显示生命周期 'a 并用于 contents 参数和返回值。
// 生命周期参数指定哪个参数与返回值的生命周期相关联。
// 这里告诉 rust 函数 search 返回的数据将与 search 函数中的参数 contents 的数据存在的一样久。
// 为了使这个引用有效那么被 slice 引用的数据也需要保持有效。
pub fn search<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    let mut results = Vec::new();

    for line in contents.lines() {
        if line.contains(query) {
            results.push(line);
        }
    }

    results
}

pub fn search_case_insensitive<'a>(query: &str, contents: &'a str) -> Vec<&'a str> {
    let query = query.to_lowercase();
    let mut results = Vec::new();

    for line in contents.lines() {
        if line.to_lowercase().contains(&query) {
            results.push(line);
        }
    }

    results
}

// Box<dyn Error> 意味着函数会返回实现了 Error trait 的类型，不过无需指定具体将会返回的值的类型。
// 这提供了在不同的错误场景可能有不同类型的错误返回值的灵活性。
// dyn 是 "动态的"（"dynamic"）的缩写。
pub fn run(config: Config) -> Result<(), Box<dyn Error>> {
    // ? 会从函数中返回错误值并让调用者来处理它。
    let contents = fs::read_to_string(config.filename)?;

    let results = if config.case_sensitive {
        search(&config.query, &contents)
    } else {
        search_case_insensitive(&config.query, &contents)
    };

    for line in results {
        println!("{}", line);
    }

    // 成功时会返回一个 Ok 值，函数的返回值中成功的返回值为 ()。
    // 使用 () 是惯用做法，表明调用 run 函数只是为了它的副作用，函数并没有返回什么有意义的值。
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn one_result() {
        let query = "duct";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.";

        assert_eq!(vec!["safe, fast, productive."], search(query, contents));
    }

    #[test]
    fn case_sensitive() {
        let query = "duct";
        let contents = "\
Rust:
safe, fast, productive.
Pick three.
Duct tape.";

        assert_eq!(vec!["safe, fast, productive."], search(query, contents));
    }

    #[test]
    fn case_insensitive() {
        let query = "rUsT";
        let contents = "\
Rust:
safe, fast, productive.
pick three.
Trust me.";

        assert_eq!(vec!["Rust:", "Trust me."], search_case_insensitive(query, contents));
    }
}

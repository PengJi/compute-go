#[macro_export]
macro_rules! my_vec {  // my_vec! 模仿 vec!
    ($($x: expr), *) => {
        {
            let mut temp_vec = Vec::new();
            $(
                temp_vec.push($x);
            )*
            temp_vec
        }
    };
}

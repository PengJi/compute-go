pub mod factory;
pub mod animal;

pub fn add(left: usize, right: usize) -> usize {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    //use animal::cat;
    //use animal::dog;
    use crate::animal::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }

    #[test]
    fn use_cat() {
        //cat::hello();
        assert_eq!(true, cat::is_cat());
    }

    #[test]
    fn use_dog() {
        //assert_eq!(true, animail::dog::is_dog());
        assert_eq!(true, dog::is_dog());
    }
}

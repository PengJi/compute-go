pub struct AverCollect {
    list: Vec<i32>,
    aver: f64,
}

impl AverCollect {
    pub fn new() -> AverCollect {
        AverCollect {
            list: vec![],
            aver: 0.0,
        }
    }

    pub fn add(&mut self, value: i32) {
        self.list.push(value);
        self.update_average();
    }

    pub fn remove(&mut self) -> Option<i32> {
        let result = self.list.pop();
        match result {
            Some(value) => {
                self.update_average();
                Some(value)
            },
            None => None,
        }
    }
    
    pub fn average(&self) -> f64 {
        self.aver
    }
}

impl AverCollect {
    fn update_average(&mut self) {  // 私有函数
        let total: i32 = self.list.iter().sum();
        self.aver = total as f64 / self.list.len() as f64;
    }
}


pub fn add(left: usize, right: usize) -> usize {
    left + right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }
}
// Draw 对象安全
pub trait Draw {
    fn draw(&self);
}

pub struct Screen {
    pub components: Vec<Box<dyn Draw>>,  // 使用 dyn 关键字指定 trait 对象
}

// void func(A *p) {
// }
// pub struct Screen<T: Draw> {
//     pub components: Vec<T>,
// }

impl Screen {
    pub fn run(&self) {
        for comp in self.components.iter() {
            comp.draw();
        }
    }
}

// trait bound，会使用静态分发
// 当使用泛型后，vec 的元素必须一致
//impl<T> Screen <T>
//    where T: Draw {
//    pub fn run(&self) {
//        for comp in self.components.iter() {
//            comp.draw();
//        }
//    }
//}

pub struct Button {
    pub width: u32,
    pub height: u32,
    pub label: String,
}

impl Draw for Button {
    fn draw(&self) {
        println!("draw button, width = {}, height = {}, label = {}", 
                 self.width, self.height, self.label);
    }
}

pub struct SelectBox {
    pub width: u32,
    pub height: u32,
    pub option: Vec<String>,
}

impl Draw for SelectBox {
    fn draw(&self) {
        println!("draw selectBox, width = {}, height = {}, option = {:?}",
                self.width, self.height, self.option);
    }
}


#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
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

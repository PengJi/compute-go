fn main() {
    type Thunk = Box<dyn Fn() + Send + 'static>;

    let f: Thunk = Box::new(|| println!("hi"));

    fn takes_long_type(f: Thunk) {
    }

    fn returns_long_type() -> Thunk {
        Box::new(|| ())
    }
}

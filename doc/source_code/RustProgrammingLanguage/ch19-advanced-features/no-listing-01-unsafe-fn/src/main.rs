fn main() {
    unsafe fn dangerous() {}

    unsafe {
        dangerous();
    }
}

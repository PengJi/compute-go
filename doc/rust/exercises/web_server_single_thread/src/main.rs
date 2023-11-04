use std::fs;
use std::io::prelude::*;
use std::net::TcpListener;
use std::net::TcpStream;

// 单线程 web server，一次只能处理一个请求

// http 的请求格式
// Method Request-URI HTTP-Version CRLF
// headers CRLF
// message-body
//
// http 的响应个数
// HTTP-Version Status-Code Reason-Phrase CRLF
// headers CRLF
// message-body

fn main() {
    // bind 返回值为 Result<T, E>
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();

    // incoming 返回一个迭代器
    // 包含 TcpStream 类型的流（stream），stream 允许我们读取客户端发来的内容，并且编写响应。
    // for 循环一次处理每个连接（一个请求响应的完整过程）
    for stream in listener.incoming() {
        let stream = stream.unwrap();

        handle_connection(stream);
    }
}

fn handle_connection(mut stream: TcpStream) {
    let mut buffer = [0; 512]; // 在栈上申请一个 512 字节的 buffer 来存放读取的内容，类型为字节数组
    stream.read(&mut buffer).unwrap();

    // 使用 b"" 转换为字节字符串"
    let get = b"GET / HTTP/1.1\r\n";
    let (status_line, filename) = if buffer.starts_with(get) {
        ("HTTP/1.1 200 OK\r\n\r\n", "hello.html")
    } else {
        ("HTTP/1.1 404 NOT FOUND\r\n\r\n", "404.html")
    };

    let contents = fs::read_to_string(filename).unwrap();
    let response = format!("{}{}", status_line, contents);

    // as_bytes() 转换为字节，stream 的 write 方法会将 &[u8] 发送给连接。
    stream.write(response.as_bytes()).unwrap();
    stream.flush().unwrap();
}

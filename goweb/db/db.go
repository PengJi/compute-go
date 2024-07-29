package main

import (
	"database/sql"
	"fmt"
	"log/slog"

	_ "github.com/go-sql-driver/mysql"

	"goweb/config"
	"goweb/logger"
)

var (
	db      *sql.DB
	dbName  string = "user"
	charset string = "utf8"
)

func initDB() (err error) {
	log := logger.GetLogger()

	dsn := fmt.Sprintf(
		"%s:%s@tcp(%s:%d)/%s?charset=%s",
		config.AppConfig.Database.User,
		config.AppConfig.Database.Password,
		config.AppConfig.Database.Host,
		config.AppConfig.Database.Port,
		dbName,
		charset,
	)
	db, err = sql.Open("mysql", dsn)
	if err != nil {
		log.Error("Failed to open database", slog.Any("err", err))
		return err
	}

	err = db.Ping()
	if err != nil {
		log.Error("connect database failed", slog.Any("err", err))
		return err
	}
	db.SetMaxOpenConns(50)
	// db.SetMaxIdleConns(20)
	fmt.Println("连接数据库成功！")
	log.Info("connect database successfully")
	return nil
}

type user struct {
	id      int
	name    string
	age     int
	address string
}

func main() {
	err := initDB()
	if err != nil {
		fmt.Println("初始化数据库失败,err", err)
		return
	}
	//新建一个user的结构体变量
	newUser := user{
		name: "赵六",
		age:  98}
	insertRow(newUser)

	//需要修改的数据库对应记录的user结构体
	updateUser := user{
		id:   7,
		name: "蜡笔小新",
		age:  98}
	updateRow(updateUser)

	//需要修改的数据库对应记录的user结构体，id不能为空
	deleteUser := user{
		id:   6,
		name: "蜡笔小新",
		age:  98}
	deleteRow(deleteUser)

	//需要修改的数据库对应记录的user结构体，id不能为空
	queryUser := user{
		id: 3}
	QueryRow(queryUser)

	// 多行查询
	queryRows()

	// 查询预处理
	prepareQueryRow()

	// 批量插入
	prepareInsertDemo()

	// 事务
	transDemo()
}

// 向数据表中插入数据
// 参数说明newUser   ----user结构体
func insertRow(newUser user) {
	//需要插入的sql语句，？表示占位参数
	sqlStr := "insert into user(name,age) values(?,?)"
	//把user结构体的name、age字段依次传给sqlStr的占位参数
	ret, err := db.Exec(sqlStr, newUser.name, newUser.age)
	if err != nil { //执行sql语句报错
		fmt.Println("插入失败,err", err)
		return
	}
	newID, err := ret.LastInsertId() //新插入数据的ID，默认为主键
	//rowsNumber, err:= ret.RowsAffected() //受影响的行数
	if err != nil {
		fmt.Println("获取id失败,err", err)
		return
	}
	fmt.Println("插入成功，id为：", newID)
}

// 更新数据
// updateUser   ----需要更新的user结构体
func updateRow(updateUser user) {
	sqlStr := "update user set age=?,name=? where id = ?"
	ret, err := db.Exec(sqlStr, updateUser.age, updateUser.name, updateUser.id)
	if err != nil {
		fmt.Printf("更新失败,err:%v\n", err)
		return
	}
	n, err := ret.RowsAffected() // 操作影响的行数
	if err != nil {
		fmt.Printf("获取影响行数失败,err:%v\n", err)
		return
	}
	fmt.Printf("更新成功，影响行数为:%d\n", n)
}

// 删除数据
// deleteUser   ----需要删除的user结构体，删除的条件还可以是 age name等等
func deleteRow(deleteUser user) {
	sqlStr := "DELETE FROM user WHERE 1=1 AND  id = ?"
	ret, err := db.Exec(sqlStr, deleteUser.id)
	if err != nil {
		fmt.Printf("删除数据失败,err:%v\n", err)
		return
	}
	n, err := ret.RowsAffected() // 操作影响的行数
	if err != nil {
		fmt.Printf("获取影响行数失败,err:%v\n", err)
		return
	}
	fmt.Printf("删除数据成功，影响行数为:%d\n", n)
}

// 查询数据
func QueryRow(queryUser user) {
	sqlStr := "SELECT id,name,age from user WHERE 1=1 AND  id = ?"
	row := db.QueryRow(sqlStr, queryUser.id)
	var u user
	//然后使用Scan()方法给对应类型变量赋值，以便取出结果,注意传入的是指针
	err := row.Scan(&u.id, &u.name, &u.age)
	if err != nil {
		fmt.Printf("获取数据错误, err:%v\n", err)
		return
	}
	fmt.Printf("查询数据成功%#v", u)
}

// 多行查询
func queryRows() {
	sqlStr := "select id,name,age from user where id>?"
	rows, err := db.Query(sqlStr, 0)
	if err != nil {
		fmt.Println("查询失败,err", err)
		return
	}
	defer rows.Close() //关闭连接
	//循环读取数据
	for rows.Next() {
		var u user
		err := rows.Scan(&u.id, &u.name, &u.age)
		if err != nil {
			fmt.Println("scan失败,err", err)
			return
		}
		fmt.Printf("id:%d	name:%s		age:%d\n", u.id, u.name, u.age)
	}
}

// 查询预处理
func prepareQueryRow() {
	sqlStr := "select id,name,age from user where id > ?"
	stmt, err := db.Prepare(sqlStr)
	if err != nil {
		fmt.Println("预处理失败,err", err)
		return
	}
	defer stmt.Close()
	rows, err := stmt.Query(0)
	if err != nil {
		fmt.Println("查询失败,err", err)
		return
	}
	defer rows.Close()
	//循环读取
	for rows.Next() {
		var u user
		err := rows.Scan(&u.id, &u.name, &u.age)
		if err != nil {
			fmt.Println("scan失败,err", err)
			return
		}
		fmt.Printf("id:%d	 name:%s	 age:%d\n", u.id, u.name, u.age)
	}
}

// 批量插入
func prepareInsertDemo() {
	sqlStr := "insert into user (name,age) values(?,?)"
	stmt, err := db.Prepare(sqlStr) // 把要执行的命令发送给MySQL服务端做预处理
	if err != nil {
		fmt.Printf("预处理失败, err:%v\n", err)
		return
	}
	defer stmt.Close()
	// 执行重复的插入命令
	for i := 10; i < 15; i++ {
		name := fmt.Sprintf("name%02d", i)
		stmt.Exec(name, i)
	}
	fmt.Println("批量插入成功")
}

func transDemo() {
	tx, err := db.Begin()
	if err != nil {
		if tx != nil {
			tx.Rollback() // 回滚
		}
		fmt.Println("事务开启失败,err", err)
		return
	}
	sql1 := "update user set age=age+? where id=?"
	_, err = tx.Exec(sql1, 2, 1)
	if err != nil {
		tx.Rollback()
		fmt.Println("sql1执行失败,err", err)
		return
	}
	sql2 := "update user set age=age-? where id=?"
	_, err = tx.Exec(sql2, 2, 2)
	if err != nil {
		tx.Rollback()
		fmt.Println("sql2执行失败,err", err)
		return
	}
	err = tx.Commit()
	if err != nil {
		tx.Rollback()
		fmt.Println("事务提交失败,err", err)
		return
	}
	fmt.Println("数据更新成功！")
}

package db

import (
	"database/sql"
	"fmt"

	_ "github.com/go-sql-driver/mysql"

	"goweb/config"
	"goweb/logger"
)

var (
	mysqldb *sql.DB
	dbName  string = "TPCD"
	charset string = "utf8"
	log            = logger.GetLogger()
)

func InitDB() (err error) {
	dsn := fmt.Sprintf(
		"%s:%s@tcp(%s:%d)/%s?charset=%s",
		config.AppConfig.Database.User,
		config.AppConfig.Database.Password,
		config.AppConfig.Database.Host,
		config.AppConfig.Database.Port,
		dbName,
		charset,
	)
	mysqldb, err = sql.Open("mysql", dsn)
	if err != nil {
		log.Error("Failed to open database", "err", err)
		return err
	}

	err = mysqldb.Ping()
	if err != nil {
		log.Error("connect database failed", "err", err)
		return err
	}
	mysqldb.SetMaxOpenConns(50)
	// db.SetMaxIdleConns(20)
	log.Info("connect database successfully", "db address", config.AppConfig.Database.Host)
	return nil
}

func TestDB() {
	newCustomer := Customer{
		C_CUSTKEY:    1500001,
		C_NAME:       "xiaoming",
		C_ADDRESS:    "beijing",
		C_NATIONKEY:  86,
		C_PHONE:      "25-989-741-2988",
		C_ACCTBAL:    711.56,
		C_MKTSEGMENT: "BUILDING",
		C_COMMENT:    "some comments"}
	insertRow(newCustomer)

	updateCustomer := Customer{
		C_CUSTKEY:    1500001,
		C_NAME:       "xiaoming",
		C_ADDRESS:    "beijing",
		C_NATIONKEY:  86,
		C_PHONE:      "25-989-741-2988",
		C_ACCTBAL:    711.56,
		C_MKTSEGMENT: "BUILDING",
		C_COMMENT:    "updated comments"}
	updateRow(updateCustomer)

	deleteCustomer := Customer{
		C_CUSTKEY:    1500001,
		C_NAME:       "xiaoming",
		C_ADDRESS:    "beijing",
		C_NATIONKEY:  86,
		C_PHONE:      "25-989-741-2988",
		C_ACCTBAL:    711.56,
		C_MKTSEGMENT: "BUILDING",
		C_COMMENT:    "some comments"}
	defer deleteRow(deleteCustomer)

	queryUser := Customer{C_CUSTKEY: 1500001}
	QueryRow(queryUser)

	queryRows()

	prepareQueryRow()

	// prepareInsertDemo()

	// transDemo()
}

func insertRow(newCustomer Customer) {
	sqlStr := "insert into customer(C_CUSTKEY, C_NAME, C_ADDRESS, C_NATIONKEY, C_PHONE, C_ACCTBAL, C_MKTSEGMENT, C_COMMENT)" +
		" values(?,?,?,?,?,?,?,?)"
	ret, err := mysqldb.Exec(sqlStr, newCustomer.C_CUSTKEY, newCustomer.C_NAME, newCustomer.C_ADDRESS, newCustomer.C_NATIONKEY,
		newCustomer.C_PHONE, newCustomer.C_ACCTBAL, newCustomer.C_MKTSEGMENT, newCustomer.C_COMMENT)
	if err != nil {
		log.Error("insert record failed", "err", err)
		return
	}

	newID, err := ret.LastInsertId()
	//rowsNumber, err:= ret.RowsAffected()
	if err != nil {
		log.Error("get primary key failed", "err", err)
		return
	}
	log.Info("insert record successfully", "primary key", newID)
}

func updateRow(updateCustomer Customer) {
	sqlStr := "update customer set C_COMMENT=? where C_CUSTKEY = ?"
	ret, err := mysqldb.Exec(sqlStr, updateCustomer.C_COMMENT)
	if err != nil {
		log.Error("udpate failed", "err", err)
		return
	}
	affectdRows, err := ret.RowsAffected()
	if err != nil {
		log.Error("get affectd rows failed", "err", err)
		return
	}
	log.Info("udpate successfully", "affected rows", affectdRows)
}

func deleteRow(deleteCustomer Customer) {
	sqlStr := "delete from customer where 1=1 AND C_CUSTKEY = ?"
	ret, err := mysqldb.Exec(sqlStr, deleteCustomer.C_CUSTKEY)
	if err != nil {
		log.Error("delete customer failed", "err", err)
		return
	}
	affectdRows, err := ret.RowsAffected()
	if err != nil {
		log.Error("get affected rows failed", "err", err)
		return
	}
	log.Info("delete customer successfully", "affected rows", affectdRows)
}

func QueryRow(queryCustomer Customer) {
	sqlStr := "SELECT C_CUSTKEY, C_NAME, C_ADDRESS from customer WHERE 1=1 AND C_CUSTKEY = ?"
	row := mysqldb.QueryRow(sqlStr, queryCustomer.C_CUSTKEY)
	var cus Customer
	err := row.Scan(&cus.C_CUSTKEY, &cus.C_NAME, &cus.C_ADDRESS)
	if err != nil {
		log.Error("query record failed", "err", err)
		return
	}
	log.Info("get record successfully", "C_CUSTKEY", cus.C_CUSTKEY, "C_NAME", cus.C_NAME, "C_ADDRESS", cus.C_ADDRESS)
}

func queryRows() {
	sqlStr := "select C_CUSTKEY, C_NAME, C_ADDRESS from customer where C_CUSTKEY<?"
	rows, err := mysqldb.Query(sqlStr, 2)
	if err != nil {
		log.Error("query record failed", "err", err)
		return
	}
	defer rows.Close()

	for rows.Next() {
		var cus Customer
		err := rows.Scan(&cus.C_CUSTKEY, &cus.C_NAME, &cus.C_ADDRESS)
		if err != nil {
			log.Error("scan record failed", "err", err)
			return
		}
		log.Info("query record successfully", "C_CUSTKEY", cus.C_CUSTKEY, "C_NAME", cus.C_NAME, "C_ADDRESS", cus.C_ADDRESS)
	}
}

func prepareQueryRow() {
	sqlStr := "select C_CUSTKEY, C_NAME, C_ADDRESS from customer where C_CUSTKEY<?"
	stmt, err := mysqldb.Prepare(sqlStr)
	if err != nil {
		log.Error("prepare query failed", "err", err)
		return
	}
	defer stmt.Close()

	rows, err := stmt.Query(2)
	if err != nil {
		log.Error("query failed", "err", err)
		return
	}
	defer rows.Close()

	for rows.Next() {
		var cus Customer
		err := rows.Scan(&cus.C_CUSTKEY, &cus.C_NAME, &cus.C_ADDRESS)
		if err != nil {
			log.Error("scan record failed", "err", err)
			return
		}
		log.Info("query record successfully", "C_CUSTKEY", cus.C_CUSTKEY, "C_NAME", cus.C_NAME, "C_ADDRESS", cus.C_ADDRESS)
	}
}

func prepareInsertDemo() {
	sqlStr := "insert into customer (C_CUSTKEY,C_NAME) values(?,?)"
	stmt, err := mysqldb.Prepare(sqlStr)
	if err != nil {
		log.Error("prepare query failed", "err", err)
		return
	}
	defer stmt.Close()
	for i := 10; i < 15; i++ {
		name := fmt.Sprintf("name%02d", i)
		stmt.Exec(i, name)
	}
	log.Info("batch insert successfully")
}

func transDemo() {
	tx, err := mysqldb.Begin()
	if err != nil {
		if tx != nil {
			tx.Rollback()
		}
		log.Error("start transaction failed", "err", err)
		return
	}

	sql1 := "update customer set C_COMMENT=? where C_CUSTKEY=?"
	_, err = tx.Exec(sql1, 2, 1)
	if err != nil {
		tx.Rollback()
		log.Error("exec sql failed", "err", err)
		return
	}
	sql2 := "update customer set C_COMMENT=? where C_CUSTKEY=?"
	_, err = tx.Exec(sql2, 2, 2)
	if err != nil {
		tx.Rollback()
		log.Error("exec sql failed", "err", err)
		return
	}
	err = tx.Commit()
	if err != nil {
		tx.Rollback()
		log.Error("commit transaction failed", "err", err)
		return
	}
	log.Info("udpate transaction successfully")
}

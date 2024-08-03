package db

import (
	_ "github.com/go-sql-driver/mysql"

	"goweb/logger"
)

var newCustomer = Customer{
	C_CUSTKEY:    1500001,
	C_NAME:       "xiaoming",
	C_ADDRESS:    "beijing",
	C_NATIONKEY:  86,
	C_PHONE:      "25-989-741-2988",
	C_ACCTBAL:    711.56,
	C_MKTSEGMENT: "BUILDING",
	C_COMMENT:    "some comments"}

func insertCustomerRow() {
	sqlStr := "insert into customer(C_CUSTKEY, C_NAME, C_ADDRESS, C_NATIONKEY, C_PHONE, C_ACCTBAL, C_MKTSEGMENT, C_COMMENT)" +
		" values(?,?,?,?,?,?,?,?)"
	ret, err := mysqldb.Exec(sqlStr, newCustomer.C_CUSTKEY, newCustomer.C_NAME, newCustomer.C_ADDRESS, newCustomer.C_NATIONKEY,
		newCustomer.C_PHONE, newCustomer.C_ACCTBAL, newCustomer.C_MKTSEGMENT, newCustomer.C_COMMENT)
	if err != nil {
		logger.Log.Error("insert record failed", "err", err)
		return
	}

	newID, err := ret.LastInsertId()
	//rowsNumber, err:= ret.RowsAffected()
	if err != nil {
		logger.Log.Error("get primary key failed", "err", err)
		return
	}
	logger.Log.Info("insert record successfully", "primary key", newID)
}

func deleteCustomerRow() {
	sqlStr := "delete from customer where 1=1 AND C_CUSTKEY = ?"
	ret, err := mysqldb.Exec(sqlStr, newCustomer.C_CUSTKEY)
	if err != nil {
		logger.Log.Error("delete customer failed", "err", err)
		return
	}
	affectdRows, err := ret.RowsAffected()
	if err != nil {
		logger.Log.Error("get affected rows failed", "err", err)
		return
	}
	logger.Log.Info("delete customer successfully", "affected rows", affectdRows)
}

func GetCustomer(name string) (Customer, error) {
	// perpare customer
	deleteCustomerRow()
	insertCustomerRow()

	// query customer by name
	sqlStr := "SELECT C_CUSTKEY, C_NAME, C_ADDRESS from customer WHERE 1=1 AND C_NAME = ?"
	row := mysqldb.QueryRow(sqlStr, name)
	var cus Customer
	err := row.Scan(&cus.C_CUSTKEY, &cus.C_NAME, &cus.C_ADDRESS)
	if err != nil {
		logger.Log.Error("query record failed", "err", err)
		return Customer{}, err
	}
	logger.Log.Info("get record successfully", "C_CUSTKEY", cus.C_CUSTKEY, "C_NAME", cus.C_NAME, "C_ADDRESS", cus.C_ADDRESS)
	return cus, nil
}

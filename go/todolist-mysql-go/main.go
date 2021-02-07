package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/mysql"
	log "github.com/sirupsen/logrus"
)

var db, _ = gorm.Open("mysql", "root:root@/todolist?charset=utf8&parseTime=True&loc=Local")

// TodoItem is Model for Storing Todo list items
type TodoItem struct {
	ID          int `gorm:"primary_key"`
	Description string
	Completed   bool
}

// HealthCheck is function for check the health of the API
func HealthCheck(w http.ResponseWriter, r *http.Request) {
	log.Info("API Health is OK")
	w.Header().Set("Content-Type", "application/json")
	io.WriteString(w, `{"alive": true}`)
}

// CreateItem is function for create a new todo list item
func CreateItem(w http.ResponseWriter, r *http.Request) {
	var t TodoItem
	err := json.NewDecoder(r.Body).Decode(&t)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	log.WithFields(log.Fields{"description": t.Description}).Info("Add new TodoItem. Saving to database.")
	todo := &TodoItem{Description: t.Description, Completed: t.Completed}
	db.Create(&todo)
	result := db.Last(&todo)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(result.Value)
}

// UpdateItem is func for update Todo Item by Id
func UpdateItem(w http.ResponseWriter, r *http.Request) {
	// Get URL parameter from mux
	vars := mux.Vars(r)
	id, _ := strconv.Atoi(vars["id"])

	// Check if TodoItem with id given exist in DB
	item := GetItemByID(id)
	if item == false {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		io.WriteString(w, `{"updated": false, "error": "Record Not Found"}`)
	} else {
		var t TodoItem
		err := json.NewDecoder(r.Body).Decode(&t)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		log.WithFields(log.Fields{"Id": id, "Description": t.Description, "Completed": t.Completed}).Info("Updating TodoItem")
		todo := &TodoItem{}
		db.First(&todo, id)
		todo.Description = t.Description
		todo.Completed = t.Completed
		db.Save(&todo)
		w.WriteHeader(http.StatusNoContent)
	}
}

// GetItemByID is func for get Todo Item by Id
func GetItemByID(ID int) bool {
	todo := &TodoItem{}
	result := db.First(&todo, ID)
	if result.Error != nil {
		log.Error(fmt.Sprintf("TodoItem with id %d not found in database", ID))
		return false
	}
	return true
}

// DeleteItem is func for delete Todo Item by Id
func DeleteItem(w http.ResponseWriter, r *http.Request) {
	// Get URL parameter from mux
	vars := mux.Vars(r)
	id, _ := strconv.Atoi(vars["id"])

	// Check if TodoItem with id given exist in DB
	item := GetItemByID(id)
	if item == false {
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		io.WriteString(w, `{"deleted": false, "error": "Record Not Found"}`)
	} else {
		log.WithFields(log.Fields{"Id": id}).Info("Deleting TodoItem")
		todo := &TodoItem{}
		db.First(&todo, id)
		db.Delete(&todo)
		w.WriteHeader(http.StatusNoContent)
	}
}

// GetAllItems is func for get all todo items
func GetAllItems(w http.ResponseWriter, r *http.Request) {
	log.Info("Get All TodoItems")
	var todos []TodoItem
	items := db.Find(&todos)
	if items.Error != nil {
		http.Error(w, items.Error.Error(), http.StatusBadRequest)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(items.Value)

}

// GetCompletedItems is func for get todo items with completed = true
func GetCompletedItems(w http.ResponseWriter, r *http.Request) {
	log.Info("Get completed TodoItems")
	completedItems := GetTodoItems(true)
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(completedItems)
}

// GetIncompletedItems is func for get todo items with completed = false
func GetIncompletedItems(w http.ResponseWriter, r *http.Request) {
	log.Info("Get incompleted TodoItems")
	incompletedItems := GetTodoItems(false)
	w.Header().Set("Content-Type", "applaication/json")
	json.NewEncoder(w).Encode(incompletedItems)
}

// GetTodoItems is func for get todo items filter by completed bool param
// params :
// completed : bool
// return interface{} of TodoItem
func GetTodoItems(completed bool) interface{} {
	var todos []TodoItem
	todoItems := db.Where("completed = ?", completed).Find(&todos).Value
	return todoItems
}

func init() {
	log.SetFormatter(&log.TextFormatter{})
	log.SetReportCaller(true)
}
func main() {
	defer db.Close()

	// db.Debug().DropTableIfExists(&TodoItem{})
	db.Debug().AutoMigrate(&TodoItem{})

	log.Info("Starting Todolist API server on port :8000")
	router := mux.NewRouter()
	router.HandleFunc("/health-check", HealthCheck).Methods("GET")
	router.HandleFunc("/todo-completed", GetCompletedItems).Methods("GET")
	router.HandleFunc("/todo-incompleted", GetIncompletedItems).Methods("GET")
	router.HandleFunc("/todo/", CreateItem).Methods("POST")
	router.HandleFunc("/todo", GetAllItems).Methods("GET")
	router.HandleFunc("/todo/{id}", UpdateItem).Methods("PUT", "PATCH")
	router.HandleFunc("/todo/{id}", DeleteItem).Methods("DELETE")
	http.ListenAndServe(":8000", router)
}

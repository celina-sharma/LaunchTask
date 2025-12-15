// -------------------- SELECT ELEMENTS --------------------
const input = document.getElementById("todo-input");
const addBtn = document.getElementById("add-btn");
const todoList = document.getElementById("todo-list");

// -------------------- FETCH TODOS FROM LOCALSTORAGE --------------------
let todos = JSON.parse(localStorage.getItem("todos")) || [];

// -------------------- RENDER TODOS --------------------
function renderTodos() {
  todoList.innerHTML = "";
  todos.forEach((todo, index) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span>${todo}</span>
      <button class="edit-btn" onclick="editTodo(${index})">Edit</button>
      <button class="delete-btn" onclick="deleteTodo(${index})">Delete</button>
    `;
    todoList.appendChild(li);
  });
}

// -------------------- ADD TODO --------------------
addBtn.addEventListener("click", () => {
  const task = input.value.trim();
  if (task === "") {
    alert("Please enter a task!");
    return;
  }

  todos.push(task);
  saveTodos();
  input.value = "";
  renderTodos();
});

// -------------------- EDIT TODO --------------------
function editTodo(index) {
  const newTask = prompt("Edit your task:", todos[index]);
  if (newTask !== null && newTask.trim() !== "") {
    todos[index] = newTask.trim();
    saveTodos();
    renderTodos();
  }
}

// -------------------- DELETE TODO --------------------
function deleteTodo(index) {
  todos.splice(index, 1);
  saveTodos();
  renderTodos();
}

// -------------------- SAVE TO LOCALSTORAGE --------------------
function saveTodos() {
  try {
    localStorage.setItem("todos", JSON.stringify(todos));
  } catch (error) {
    console.error("LocalStorage Error:", error);
  }
}

// -------------------- INITIAL RENDER --------------------
renderTodos();
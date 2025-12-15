
## Error 1: LocalStorage Not Saving Data
**Problem:** Data was not saved after refreshing the page.  
**Cause:** LocalStorage stores only strings, but I tried saving an array directly.  
**Fix:** Used `JSON.stringify()` while saving and `JSON.parse()` while reading.

---

## Error 2: Function Not Defined (editTodo / deleteTodo)
**Problem:** Console showed “function not defined” when clicking buttons.  
**Cause:** Functions were not in the global scope for inline `onclick`.  
**Fix:** Defined `editTodo()` and `deleteTodo()` in the global scope.

---

## Error 3: Todo List Not Updating
**Problem:** UI did not update after adding, editing, or deleting tasks.  
**Cause:** The `renderTodos()` function was not called after updates.  
**Fix:** Called `renderTodos()` after every add, edit, and delete action.

---

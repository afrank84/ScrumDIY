document.addEventListener('DOMContentLoaded', function() {
    // Fetch existing tasks from the server
    fetch('/tasks')
        .then(response => response.json())
        .then(tasks => {
            tasks.forEach(task => addTaskToDOM(task));
        });

    // Add a new task
    document.getElementById('taskForm').addEventListener('submit', function(event) {
        event.preventDefault();

        const title = document.getElementById('taskTitle').value;
        const description = document.getElementById('taskDescription').value;

        fetch('/add-task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title: title, description: description })
        })
        .then(response => response.json())
        .then(task => {
            addTaskToDOM(task);
            document.getElementById('taskForm').reset();
        });
    });

    function addTaskToDOM(task) {
        const taskList = document.getElementById(`${task.status}List`);
        const listItem = document.createElement('li');
        listItem.textContent = `${task.title}: ${task.description}`;
        taskList.appendChild(listItem);
    }
});


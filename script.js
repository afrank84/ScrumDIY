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
        listItem.className = 'list-group-item';
        listItem.textContent = `${task.title}: ${task.description}`;
        listItem.draggable = true;
        listItem.id = `task-${task.id}`;
        listItem.ondragstart = drag;
        taskList.appendChild(listItem);
    }

    // Drag and Drop functionality
    window.allowDrop = function(event) {
        event.preventDefault();
    };

    window.drag = function(event) {
        event.dataTransfer.setData("text", event.target.id);
    };

    window.drop = function(event) {
        event.preventDefault();
        const taskId = event.dataTransfer.getData("text");
        const listItem = document.getElementById(taskId);
        const newStatus = event.target.closest('.column').id;

        // Update the status in the DOM
        event.target.appendChild(listItem);

        // Update the status in the database
        const id = taskId.split('-')[1];
        fetch(`/update-task/${id}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
        }).then(response => {
            if (response.ok) {
                console.log('Task status updated.');
            } else {
                console.error('Failed to update task status.');
            }
        });
    };
});

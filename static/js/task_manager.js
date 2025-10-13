class TaskManager {
    constructor() {
        this.tasks = [];
        this.init();
    }
    
    init() {
        this.loadTasks();
        this.setupWebSocket();
        this.setupEventListeners();
    }
    
    async loadTasks() {
        try {
            const response = await fetch('/api/my-tasks/');
            const data = await response.json();
            this.tasks = data.tasks;
            this.renderTasks();
            this.updateLastUpdated();
        } catch (error) {
            console.error('Ошибка загрузки задач:', error);
            this.showError('Не удалось загрузить задачи');
        }
    }
    
    renderTasks() {
        const container = document.getElementById('tasks-container');
        
        if (this.tasks.length === 0) {
            container.innerHTML = `
                <div class="feature-card" style="text-align: center;">
                    <h3>🎉 Нет задач!</h3>
                    <p>Все задачи выполнены или тебе пока не назначили новые задачи</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = this.tasks.map(task => `
            <div class="task-card ${task.status} ${task.is_overdue ? 'overdue' : ''}">
                <div class="task-header">
                    <h3>${this.escapeHtml(task.title)}</h3>
                    <span class="task-status">${this.getStatusText(task.status)}</span>
                </div>
                
                <div class="task-body">
                    ${task.description ? `<p>${this.escapeHtml(task.description)}</p>` : ''}
                    
                    <div class="task-meta">
                        <div class="meta-item">
                            <strong>📅 Срок:</strong> ${task.due_date}
                        </div>
                        <div class="meta-item">
                            <strong>🕐 Создана:</strong> ${task.created_at}
                        </div>
                    </div>
                </div>
                
                <div class="task-actions">
                    ${task.status !== 'completed' ? 
                        `<button onclick="taskManager.completeTask(${task.id})" class="btn btn-success">
                            ✅ Завершить
                        </button>` : 
                        '<span class="completed-badge">✅ Выполнена</span>'
                    }
                </div>
            </div>
        `).join('');
    }
    
    async completeTask(taskId) {
        if (!confirm('Отметить задачу как выполненную?')) return;
        
        try {
            const response = await fetch(`/api/complete-task/${taskId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCSRFToken(),
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showMessage('✅ Задача отмечена как выполненная!');
                this.loadTasks();
            } else {
                this.showError(data.error || 'Ошибка при завершении задачи');
            }
        } catch (error) {
            console.error('Ошибка:', error);
            this.showError('Не удалось завершить задачу');
        }
    }
    
    setupWebSocket() {
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${wsProtocol}//${window.location.host}/ws/tasks/`;
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            console.log('WebSocket connected');
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleWebSocketMessage(data);
        };
        
        this.ws.onclose = () => {
            console.log('WebSocket disconnected');
            setTimeout(() => this.setupWebSocket(), 5000);
        };
    }
    
    handleWebSocketMessage(data) {
        switch(data.type) {
            case 'task_created':
                this.showMessage(`📨 Новая задача: ${data.task.title}`);
                this.loadTasks();
                break;
                
            case 'task_update':
                this.showMessage(`🔄 Задача обновлена: ${data.task.title}`);
                this.loadTasks();
                break;
                
            case 'task_completed':
                this.showMessage('✅ Задача завершена!');
                this.loadTasks();
                break;
        }
    }
    
    getStatusText(status) {
        const statusMap = {
            'pending': '⏳ Ожидает',
            'in_progress': '🔄 В работе', 
            'completed': '✅ Завершена'
        };
        return statusMap[status] || status;
    }
    
    updateLastUpdated() {
        const element = document.getElementById('last-updated');
        if (element) {
            element.textContent = `Обновлено: ${new Date().toLocaleTimeString()}`;
        }
    }
    
    showMessage(message) {
        alert(message);
    }
    
    showError(message) {
        alert(`❌ ${message}`);
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    getCSRFToken() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    setupEventListeners() {
        setInterval(() => this.loadTasks(), 30000);
    }
}

// Глобальная переменная для доступа из HTML
const taskManager = new TaskManager();

// Глобальная функция для кнопки обновления
function loadTasks() {
    taskManager.loadTasks();
}
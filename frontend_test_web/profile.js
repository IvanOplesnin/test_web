// Получаем токен из localStorage
const token = localStorage.getItem('access_token');
const access_token = JSON.parse(token).access_token

// Если токена нет - перенаправляем на страницу входа
if (!token) {
    window.location.href = 'login.html';
}


// Конфигурация API
const API_BASE_URL = 'http://localhost:8000';
const headers = {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
};

// Элементы DOM
const logoutBtn = document.getElementById('logoutBtn');
const refreshAccountsBtn = document.getElementById('refreshAccounts');
const refreshTransactionsBtn = document.getElementById('refreshTransactions');


async function makeAuthRequest(url, options = {}) {
    try {
        // Добавляем токен в заголовки
        const authHeaders = {
            'Authorization': `Bearer ${access_token}`,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };

        // Выполняем запрос
        const response = await fetch(url, {
            ...options,
            headers: {
                ...authHeaders,
                ...options.headers // Позволяет переопределить заголовки
            },
            body: options.body ? JSON.stringify(options.body) : null
        });
        

        // Обработка 401 Unauthorized
        if (response.status === 401) {
            redirectToLogin();
            return null;
        }

        // Проверка на другие ошибки
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Парсим JSON только если есть тело ответа
        return response.status !== 204 ? await response.json() : null;
        
    } catch (error) {
        console.error('Request failed:', error);
        
        // Перенаправляем при проблемах с авторизацией
        if (error.message.includes('401') || error instanceof TypeError) {
            redirectToLogin();
        }
        
        throw error; // Пробрасываем ошибку для дальнейшей обработки
    }
}

// Функция для выхода
function redirectToLogin() {
    localStorage.removeItem('access_token');
    window.location.href = 'login.html';
}

// Показать/скрыть админ-панель
function toggleAdminPanel(isAdmin) {
    const adminSection = document.getElementById('adminSection');
    adminSection.style.display = isAdmin ? 'block' : 'none';
    if (isAdmin) {
        loadAllUsers();
    }
}

// Загрузка всех пользователей
async function loadAllUsers() {
    const tbody = document.getElementById('usersList');
    tbody.innerHTML = '<tr><td colspan="7" class="text-center">Loading...</td></tr>';
    
    try {
        const users = await makeAuthRequest(`${API_BASE_URL}/admin/all_users`);
        if (!users || !Array.isArray(users)) {
            throw new Error('Invalid data received');
        }
        
        if (users.length === 0) {
            showError('usersList', 'No users found');
            return;
        }
        renderUsersTable(users);
        renderAllAccounts(users);
    } catch (error) {
        console.error('Error loading users:', error);
        showError('usersList', 'Failed to load users');
    }
}

function renderUsersTable(users) {
    const tbody = document.getElementById('usersList');
    tbody.innerHTML = '';
    
    users.forEach(user => {
        const accountsCount = user.accounts?.length || 0;
        const transactionsCount = user.accounts?.reduce(
            (sum, acc) => sum + (acc.transactions?.length || 0), 0
        );
        
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.id}</td>
            <td>${escapeHtml(user.fullname)}</td>
            <td>${escapeHtml(user.email)}</td>
            <td>${user.is_admin ? '<span class="badge bg-danger">Админ</span>' : 
                '<span class="badge bg-secondary">Пользователь</span>'}</td>
            <td>${accountsCount}</td>
            <td>${transactionsCount}</td>
            <td>
                <button class="btn btn-sm btn-outline-primary view-details" 
                    data-userid="${user.id}">
                    <i class="bi bi-eye"></i> Детали
                </button>
                <button class="btn btn-sm btn-warning edit-user" data-id="${user.id}">
                    <i class="bi bi-pencil"></i>
                </button>
                <button class="btn btn-sm btn-danger delete-user" data-id="${user.id}">
                    <i class="bi bi-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);        
    });
    document.querySelectorAll('.edit-user').forEach(btn => {
        btn.addEventListener('click', () => showEditUserForm(btn.dataset.id))
    })
}

function renderAllAccounts(users) {
    const tbody = document.getElementById('allAccountsList');
    tbody.innerHTML = '';
    
    users.forEach(user => {
        user.accounts?.forEach(account => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${account.id}</td>
                <td>${user.fullname} (ID: ${user.id})</td>
                <td>${account.balance.toFixed(2)}</td>
            `;
            tbody.appendChild(row);
        });
    });
}


// Показать форму создания/редактирования
async function showEditUserForm(userId = null) {
    const modal = new bootstrap.Modal(document.getElementById('userModal'));
    const form = document.getElementById('userForm');

    if (userId) {
        document.getElementById('modalTitle').textContent = 'Редактировать пользователя';
        document.getElementById('userId_modal').value = userId;
        
        try {
            const user = await makeAuthRequest(`${API_BASE_URL}/admin/all_users`);
            if (user) {
                const foundUser = user.find(u => u.id == userId);
                if (foundUser) {
                    document.getElementById('fullname_modal').value = foundUser.fullname;
                    document.getElementById('email_modal').value = foundUser.email;
                    document.getElementById('isAdmin_modal').checked = foundUser.is_admin;
                    document.getElementById('password_modal').value = '';
                }
            }
        } catch (error) {
            console.error('Ошибка загрузки данных пользователя:', error);
        }
    } else {
        document.getElementById('modalTitle').textContent = 'Добавить пользователя';
        form.reset();
        document.getElementById('password_modal').value = '';
    }
    
    modal.show();
}


// Сохранить пользователя
async function saveUser() {
    const userId = document.getElementById('userId_modal').value;
    const isEdit = !!userId;
    
    const userData = {
        fullname: document.getElementById('fullname_modal').value,
        email: document.getElementById('email_modal').value,
        is_admin: document.getElementById('isAdmin_modal').checked,
    };

    // Добавляем пароль только если он есть (для создания) или изменён (для редактирования)
    const password = document.getElementById('password_modal').value;
    if ((!isEdit && password) || (isEdit && password.length > 6)) {
        userData.password = password;
    }

    
    try {
        let response;
        if (isEdit) {
            response = await makeAuthRequest(`${API_BASE_URL}/admin/update_user/${userId}`, {
                method: 'PATCH',
                body: userData
            });
        } else {
            response = await makeAuthRequest(`${API_BASE_URL}/admin/create_user`, {
                method: 'POST',
                body: userData
            });
        }
        
        if (response) {
            bootstrap.Modal.getInstance(document.getElementById('userModal')).hide();
            loadAllUsers();
        }
    } catch (error) {
        console.error('Ошибка сохранения пользователя:', error);
        alert('Ошибка сохранения пользователя');
    }
}


// Удалить пользователя
async function deleteUser(userId) {
    if (!confirm('Вы уверены, что хотите удалить этого пользователя?')) return;
    
    try {
        const response = await makeAuthRequest(`${API_BASE_URL}/admin/delete_user/${userId}`, {
            method: 'DELETE'
        });
        
        if (response !== undefined) { // DELETE может не возвращать тело
            loadAllUsers();
        }
    } catch (error) {
        console.error('Ошибка удаления пользователя:', error);
        alert('Ошибка удаления пользователя');
    }
}

logoutBtn.addEventListener('click', () => {
    redirectToLogin()
});

// Обновите функцию loadUserInfo для показа админ-панели
async function loadUserInfo() {
    try {
        const user = await makeAuthRequest(`${API_BASE_URL}/users/info`, {
            method: 'GET'
        });
        if (!user) return;
        
        document.getElementById('fullname').textContent = user.fullname;
        document.getElementById('email').textContent = user.email;
        document.getElementById('userId').textContent = user.id;
        document.getElementById('isAdmin').textContent = user.is_admin ? 'Администратор' : 'Обычный пользователь';
        
        // Показать админ-панель если пользователь админ
        toggleAdminPanel(user.is_admin);
        
    } catch (error) {
        console.error('Ошибка:', error);
        document.getElementById('userInfo').innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger">Не удалось загрузить данные пользователя</div>
            </div>
        `;
    }
}

// Загрузка счетов пользователя
async function loadAccounts() {
    const accountsList = document.getElementById('accountsList');
    accountsList.innerHTML = '<div class="col-12"><div class="alert alert-info">Загрузка данных...</div></div>';
    
    try {
        const accounts = await makeAuthRequest(`${API_BASE_URL}/users/accounts`, { 
            method: "GET"
         });
        
        if (accounts.length === 0) {
            accountsList.innerHTML = '<div class="col-12"><div class="alert alert-warning">У вас пока нет счетов</div></div>';
            return;
        }
        
        let html = '';
        accounts.forEach(account => {
            html += `
                <div class="col-md-4 mb-3">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">Счет #${account.id}</h5>
                            <p class="card-text">
                                <strong>ID:</strong> ${account.id}<br>
                                <strong>Баланс:</strong> ${account.balance} руб.<br>
                            </p>
                        </div>
                    </div>
                </div>
            `;
        });
        
        accountsList.innerHTML = html;
    } catch (error) {
        console.error('Ошибка:', error);
        accountsList.innerHTML = '<div class="col-12"><div class="alert alert-danger">Ошибка загрузки счетов</div></div>';
    }
}

// Загрузка транзакций пользователя
async function loadTransactions() {
    const transactionsList = document.getElementById('transactionsList');
    transactionsList.innerHTML = '<div class="alert alert-info">Загрузка данных...</div>';
    
    try {
        const transactions = await makeAuthRequest(`${API_BASE_URL}/users/transactions`, { 
            method: "GET"
         });
        
        if (transactions.length === 0) {
            transactionsList.innerHTML = '<div class="alert alert-warning">У вас пока нет транзакций</div>';
            return;
        }
        
        let html = '';
        transactions.forEach(transaction => {
            const amountClass = transaction.amount >= 0 ? 'positive-amount' : 'negative-amount';
            html += `
                <div class="card mb-2 transaction-item">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6 class="card-subtitle mb-1">ID-Транзакции ${transaction.id}</h6>
                                <p class="card-text mb-1">
                                    <strong>Счет:</strong> ${transaction.account_id}<br>
                                    <strong>ID-Транзакции(платежной системы):</strong> ${transaction.transaction_id}
                                </p>
                            </div>
                            <div class="text-end">
                                <p class="card-text mb-1"><strong>Сумма:</strong> 
                                    <span class="${amountClass}">${transaction.amount} руб.</span>
                                </p>
                            </div>
                        </div>
                        ${transaction.description ? `<p class="card-text mt-2"><em>${transaction.description}</em></p>` : ''}
                    </div>
                </div>
            `;
        });
        
        transactionsList.innerHTML = html;
    } catch (error) {
        console.error('Ошибка:', error);
        transactionsList.innerHTML = '<div class="alert alert-danger">Ошибка загрузки транзакций</div>';
    }
}

// Обработчики кнопок обновления
refreshAccountsBtn.addEventListener('click', loadAccounts);
refreshTransactionsBtn.addEventListener('click', loadTransactions);


// Экранирование HTML
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Показать ошибку
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-danger">${message}</td>
            </tr>
        `;
    }
}

// Инициализация страницы
document.addEventListener('DOMContentLoaded', () => {
    loadUserInfo();
    loadAccounts();
    
    // Загружаем транзакции при переходе на вкладку
    document.getElementById('transactions-tab').addEventListener('shown.bs.tab', loadTransactions);
    document.getElementById('createUserBtn').addEventListener('click', () => showEditUserForm());
    document.getElementById('saveUserBtn').addEventListener('click', saveUser);
    document.querySelectorAll('.edit-user').forEach(btn => {
        btn.addEventListener('click', () => showEditUserForm(btn.data-id))
    })

    document.querySelectorAll('#refreshAdminData').forEach(btn => {
        btn.addEventListener('click', loadAllUsers);
    });

    // Обработчики переключения вкладок
    document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
        tab.addEventListener('shown.bs.tab', () => {
            if (allUsersData.length > 0) {
                renderAllAccounts(allUsersData);
            }
        });
    });
});
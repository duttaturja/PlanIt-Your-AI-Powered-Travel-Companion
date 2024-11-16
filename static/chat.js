// Selecting DOM elements
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const sidebar = document.getElementById('sidebar');
const sidebarToggler = document.getElementById('sidebarToggler');
const profileButton = document.getElementById('profileButton');
const profileDropdown = document.getElementById('profileDropdown');
const overlay = document.getElementById('overlay');

// User and Bot Data
const users = {
    user: { name: 'You', avatar: 'https://via.placeholder.com/40' },
    bot: { name: 'PlanIt', avatar: 'https://via.placeholder.com/40?text=Bot' }
};

// Function to add a message
function addMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('flex', 'items-start', 'mb-4');

    const avatarElement = document.createElement('img');
    avatarElement.src = users[sender].avatar;
    avatarElement.alt = `${users[sender].name}'s avatar`;
    avatarElement.classList.add('w-10', 'h-10', 'rounded-full', 'mr-3');

    const contentElement = document.createElement('div');
    contentElement.classList.add('flex', 'flex-col');

    const nameElement = document.createElement('span');
    nameElement.textContent = users[sender].name;
    nameElement.classList.add('font-semibold', 'mb-1');

    const textElement = document.createElement('p');
    textElement.textContent = message;
    textElement.classList.add('bg-gray-200', 'rounded-lg', 'p-2', sender === 'user' ? 'text-right' : '');

    contentElement.appendChild(nameElement);
    contentElement.appendChild(textElement);

    messageElement.appendChild(avatarElement);
    messageElement.appendChild(contentElement);

    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to show typing indicator
function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator flex items-center space-x-1';
    indicator.innerHTML = `
        <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
        <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
        <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
    `;
    chatMessages.appendChild(indicator);
    return indicator;
}

// Event Listeners
sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
        addMessage('user', message);
        userInput.value = '';
        const typingIndicator = showTypingIndicator();

        // Simulate bot response
        setTimeout(() => {
            typingIndicator.remove();
            addMessage('bot', 'This is a sample bot response.');
        }, 2000);
    }
}

// Sidebar toggle
sidebarToggler.addEventListener('click', () => {
    sidebar.classList.toggle('-translate-x-full');
    overlay.classList.toggle('hidden');
});

// Overlay click to close sidebar
overlay.addEventListener('click', () => {
    sidebar.classList.add('-translate-x-full');
    overlay.classList.add('hidden');
});

// Profile dropdown toggle
profileButton.addEventListener('click', () => {
    profileDropdown.classList.toggle('hidden');
});

// Initial bot message
addMessage('bot', 'Hello! How can I assist you today?');

document.addEventListener("DOMContentLoaded", () => {
    const voiceHistoryList = document.getElementById('voice-history-list');
    const searchHistoryList = document.getElementById('search-history-list');
    const deleteVoiceButton = document.getElementById('delete-voice-history');
    const deleteSearchButton = document.getElementById('delete-search-history');

    const loadHistory = (type) => {
        const historyList = type === 'voice' ? voiceHistoryList : searchHistoryList;
        const storageKey = type === 'voice' ? 'voiceHistory' : 'searchHistory';
        const historyData = JSON.parse(localStorage.getItem(storageKey)) || [];
        historyList.innerHTML = '';
        historyData.forEach(entry => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<strong>${entry.timestamp}:</strong> <br>Input: ${entry.input}<br>Result: ${entry.result}`;
            historyList.appendChild(listItem);
        });
    };

    deleteVoiceButton.addEventListener('click', () => {
        localStorage.removeItem('voiceHistory');
        loadHistory('voice');
    });

    deleteSearchButton.addEventListener('click', () => {
        localStorage.removeItem('searchHistory');
        loadHistory('search');
    });

    loadHistory('voice');
    loadHistory('search');
});

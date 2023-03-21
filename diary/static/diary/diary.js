const deleteButton = document.querySelector('.diary-delete-button');
deleteButton.addEventListener('click', (event) => {
  event.preventDefault();
  if (confirm("本当に削除しますか？")) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = deleteButton.href;
    form.innerHTML = `<input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">`;
    document.body.appendChild(form);
    form.submit();
  }
});
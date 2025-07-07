function openDeleteModal(id) {
  document.getElementById('delete_id').value = id;
  document.getElementById('admin_username').value = '';
  document.getElementById('admin_password').value = '';
  document.getElementById('confirm_checkbox').checked = false;
  document.getElementById('deleteModal').classList.remove('hidden');
}

function closeDeleteModal() {
  document.getElementById('deleteModal').classList.add('hidden');
}

function validateDeleteForm() {
  if (!document.getElementById('confirm_checkbox').checked) {
    alert("Please confirm deletion by checking the box.");
    return false;
  }
  return true;
}


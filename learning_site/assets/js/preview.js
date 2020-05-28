document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('id_description');
  const preview = document.getElementById('preview');
  preview.innerHTML = marked(input.value);
});

$('.order').sortable({
  filter: '.new',
  onUpdate: function(e) {
    $.each($(e.item).parent().find('.item'), function(index, item) {
      $(item).find('[name$="order"]').val(index);
    });
  },
});

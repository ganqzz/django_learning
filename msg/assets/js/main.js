/**
 * モーダルウィンドウ
 * @property {HTMLElement} modal モーダル要素
 * @property {NodeList} openers モーダルを開く要素
 * @property {NodeList} closers モーダルを閉じる要素
 */
function Modal(modal) {
  this.modal = modal;
  const id = this.modal.id;
  this.openers = document.querySelectorAll('[data-modal-open="' + id + '"]');
  this.closers = this.modal.querySelectorAll('[data-modal-close]');

  // 開くボタンのイベント登録
  this.openers.forEach(opener => {
    opener.addEventListener('click', this.open.bind(this));
  });

  // 閉じるボタンのイベント登録
  this.closers.forEach(closer => {
    closer.addEventListener('click', this.close.bind(this));
  });
}

/**
 * モーダルを開く
 */
Modal.prototype.open = function() {
  this.modal.classList.add('show');
};

/**
 * モーダルを閉じる
 */
Modal.prototype.close = function() {
  this.modal.classList.remove('show');
};

/**
 * モーダル登録
 */
document.addEventListener('DOMContentLoaded', () => {
  const elem = document.getElementById('modal-post-form');
  new Modal(elem);
});


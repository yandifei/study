const request = require('../../utils/request.js');
const { API } = require('../../config/api.js');

/** "2026-06-10T17:41:23.423000" → "2026年06月10日 17:41" */
function fmtTime(iso) {
  if (!iso) return '';
  const [date, time] = iso.split('T');
  const [y, m, d] = date.split('-');
  return `${y}年${m}月${d}日 ${time.slice(0, 5)}`;
}

function fmtList(records) {
  return (records || []).map(r => ({ ...r, displayTime: fmtTime(r.favorite_time) }));
}

Page({
  data: {
    list: [],
    loading: true,
    loadingMore: false,
    skip: 0,
    limit: 20,
    hasMore: true
  },

  onShow() {
    if (this._justPreviewed) {
      this._justPreviewed = false;
      return;
    }
    this.setData({ skip: 0, hasMore: true, list: [] });
    this.loadList();
  },

  /** 加载收藏列表（首次加载替换，触底追加） */
  loadList() {
    const { skip, limit, list } = this.data;
    const isAppend = skip > 0;

    if (!isAppend) {
      this.setData({ loading: true });
    } else {
      this.setData({ loadingMore: true });
    }

    request.get(API.FAVORITE_LIST, { data: { limit, skip } })
      .then(res => {
        if (res.statusCode === 200) {
          const records = res.data.data.records;
          const data = fmtList(records);
          this.setData({
            list: isAppend ? [...list, ...data] : data,
            loading: false,
            loadingMore: false,
            skip: skip + records.length,
            hasMore: records.length >= limit
          });
        } else {
          if (!isAppend) this.setData({ loading: false });
          else this.setData({ loadingMore: false });
        }
      })
      .catch(() => {
        if (!isAppend) {
          this.setData({ loading: false });
          wx.showToast({ title: '加载失败', icon: 'none' });
        } else {
          this.setData({ loadingMore: false });
        }
      });
  },

  /** 触底加载更多 */
  onReachBottom() {
    if (!this.data.hasMore || this.data.loading) return;
    this.loadList();
  },

  /** 页面级下拉刷新 */
  onPullDownRefresh() {
    this.setData({ skip: 0, hasMore: true, list: [] });
    this.loadList().finally(() => wx.stopPullDownRefresh());
  },

  /** 清空所有收藏 */
  clearAll() {
    wx.showModal({
      title: '确认清空',
      content: '确定要清空所有收藏吗？此操作不可恢复。',
      confirmText: '确定清空',
      cancelText: '取消',
      confirmColor: '#e07050',
      success: (res) => {
        if (res.confirm) {
          request.delete(API.FAVORITE_CLEAR)
            .then(() => {
              wx.showToast({ title: '已清空', icon: 'success' });
              this.setData({ list: [] });
            })
            .catch(() => wx.showToast({ title: '操作失败', icon: 'none' }));
        }
      }
    });
  },

  /** 取消单个收藏 —— DELETE /favorite/{image_id} */
  removeOne(e) {
    const imageId = e.currentTarget.dataset.id;
    if (!imageId) return;

    wx.showModal({
      title: '取消收藏',
      content: '确定要取消收藏这张图片吗？',
      confirmText: '确定',
      cancelText: '再想想',
      confirmColor: '#e07050',
      success: (res) => {
        if (res.confirm) {
          request.delete(API.FAVORITE_REMOVE + imageId)
            .then(() => {
              wx.showToast({ title: '已取消收藏', icon: 'success' });
              const newList = this.data.list.filter(item => item.image_id !== imageId);
              this.setData({ list: newList });
            })
            .catch(() => wx.showToast({ title: '操作失败', icon: 'none' }));
        }
      }
    });
  },

  /** 保存图片到相册 */
  saveImage(e) {
    const imgUrl = e.currentTarget.dataset.url;
    if (!imgUrl) return;
    wx.downloadFile({
      url: imgUrl,
      success: (res) => {
        wx.saveImageToPhotosAlbum({
          filePath: res.tempFilePath,
          success() {
            wx.showToast({ title: '保存成功', icon: 'success' });
          },
          fail() {
            wx.showToast({ title: '保存失败', icon: 'none' });
          }
        });
      },
      fail() {
        wx.showToast({ title: '下载失败', icon: 'none' });
      }
    });
  },

  /** 点击预览大图 */
  previewImage(e) {
    this._justPreviewed = true;
    const url = e.currentTarget.dataset.url;
    const urls = this.data.list.map(item => item.image_url);
    wx.previewImage({ urls, current: url });
  }
});

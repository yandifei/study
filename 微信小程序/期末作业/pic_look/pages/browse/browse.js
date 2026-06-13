const request = require('../../utils/request.js');
const { API } = require('../../config/api.js');

const PAGE_SIZE = 20;

/** "2026-06-10T17:41:23.423000" → "06-10 17:41" */
function fmtTime(iso) {
  return iso ? iso.slice(5, 16).replace('T', ' ') : '';
}

function fmtList(records) {
  return (records || []).map(r => ({ ...r, displayTime: fmtTime(r.browse_time) }));
}

Page({
  data: {
    list: [],
    loading: true,
    skip: 0,
    hasMore: true,
    loadingMore: false
  },

  onShow() {
    // 预览大图返回时不重复刷新
    if (this._justPreviewed) {
      this._justPreviewed = false;
      return;
    }
    this.loadList();
  },

  /** 首次加载：重置 skip，替换列表 */
  loadList() {
    this.setData({ loading: true, skip: 0, hasMore: true });

    request.get(API.BROWSE_LIST + `?limit=${PAGE_SIZE}&skip=0`)
      .then(res => {
        if (res.statusCode === 200) {
          const data = fmtList(res.data.data.records);
          this.setData({
            list: data,
            loading: false,
            skip: data.length,
            hasMore: data.length >= PAGE_SIZE
          });
        } else {
          this.setData({ loading: false });
        }
      })
      .catch(() => {
        this.setData({ loading: false });
        wx.showToast({ title: '加载失败', icon: 'none' });
      });
  },

  /** 页面级下拉刷新（只有从顶部下拉才触发） */
  onPullDownRefresh() {
    request.get(API.BROWSE_LIST + `?limit=${PAGE_SIZE}&skip=0`)
      .then(res => {
        if (res.statusCode === 200) {
          const data = fmtList(res.data.data.records);
          this.setData({
            list: data,
            skip: data.length,
            hasMore: data.length >= PAGE_SIZE
          });
        }
        wx.stopPullDownRefresh();
      })
      .catch(() => wx.stopPullDownRefresh());
  },

  /** 触底加载更多 */
  onReachBottom() {
    if (!this.data.hasMore || this.data.loadingMore) return;

    this.setData({ loadingMore: true });
    const skip = this.data.skip;

    request.get(API.BROWSE_LIST + `?limit=${PAGE_SIZE}&skip=${skip}`)
      .then(res => {
        if (res.statusCode === 200) {
          const data = fmtList(res.data.data.records);
          const newList = [...this.data.list, ...data];
          this.setData({
            list: newList,
            skip: skip + data.length,
            hasMore: data.length >= PAGE_SIZE,
            loadingMore: false
          });
        } else {
          this.setData({ loadingMore: false });
        }
      })
      .catch(() => {
        this.setData({ loadingMore: false });
        wx.showToast({ title: '加载失败', icon: 'none' });
      });
  },

  /** 清空所有浏览记录 */
  clearAll() {
    wx.showModal({
      title: '确认清空',
      content: '确定要清空所有浏览记录吗？此操作不可恢复。',
      confirmText: '确定清空',
      cancelText: '取消',
      confirmColor: '#5daa82',
      success: (res) => {
        if (res.confirm) {
          request.delete(API.BROWSE_CLEAR)
            .then(() => {
              wx.showToast({ title: '已清空', icon: 'success' });
              this.setData({ list: [], skip: 0, hasMore: false });
            })
            .catch(() => wx.showToast({ title: '操作失败', icon: 'none' }));
        }
      }
    });
  },

  /** 点击预览大图 —— 微信原生查看器自带保存/分享 */
  previewImage(e) {
    this._justPreviewed = true;
    const url = e.currentTarget.dataset.url;
    const urls = this.data.list.map(item => item.image_url);
    wx.previewImage({ urls, current: url });
  }
});

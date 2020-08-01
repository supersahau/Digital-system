//pages/test/test.js
var app = getApp();
Page({

  /**
   * 页面的初始数据
   */
  data: {
    article: '',
    responseID: '',
    PostAccount: '',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

  
  URLInput: function (e) {
    this.setData({
      article: 'url=' + e.detail.value
    })

  },

  AccountInput: function (e) {
    this.setData({
      PostAccount: 'account=' + encodeURI(e.detail.value)
    })

  },
//application/x-www-form-urlencoded
  uploadurl: function () {

    var that = this;
    wx.request({
      url: 'http://111.231.71.74:8888/posturl',
      data: that.data.article,
      header: {
        'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
      },
      method: 'POST',
      success: function (res) {
        console.log('submit success');
        console.log(res.data);
        app.globalData.globalID = res.data;
        that.setData({
          responseID: 'id=' + res.data
        })
      },
      fail: function (res) {
        console.log('submit fail');
      },
      complete: function (res) {
        console.log('submit complete');
      }

    })
  },
  Exception: function(){
    var that = this;
    wx.request({
      url: 'http://111.231.71.74:8888/postaccount',
      data: that.data.responseID +'&' + that.data.PostAccount,
      header: {
        'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
      },
      method: 'POST',
      success: function (res) {
        console.log('submit success');
        console.log(res.data);
        app.globalData.jsonlist = res.data;
        console.log(app.globalData.jsonlist);
        for (var i = 0; i < res.data.comment.length; i++) {
          app.globalData.jsonlist.comment[i].pt = app.globalData.jsonlist.comment[i].pt.slice(0,4);
          }
        wx.switchTab({
          url: '../../pages/exception/exception',
        })
        
      },
      fail: function (res) {
        console.log('submit fail');
      },
      complete: function (res) {
        console.log('submit complete');
      }
  })
  },
  recommend: function(){
    var that = this
    wx.request({
      url: 'http://111.231.71.74:8888/recommend',
      data: {
        'id':app.globalData.globalID,
      },
      header: {
         'content-type': 'application/json'
       },
      method: 'GET',
      success: function (res) {
        console.log('submit success');
        console.log(res.data);
        app.globalData.recommendList = res.data;
        for (var i=0;i<res.data.length;i++){
          app.globalData.recommendList[i].url = escape(app.globalData.recommendList[i].url);
          if (app.globalData.recommendList[i].title.length > 42){
            app.globalData.recommendList[i].title = app.globalData.recommendList[i].title.slice(0,42) + '...';
          }
        };
        console.log(app.globalData.recommendList);
        wx.switchTab({
          url: '../../pages/list/list'
        });
      },
      fail: function (res) {
        console.log('submit fail');
      },
      complete: function (res) {
        console.log('submit complete');
      }
    })
  }

})
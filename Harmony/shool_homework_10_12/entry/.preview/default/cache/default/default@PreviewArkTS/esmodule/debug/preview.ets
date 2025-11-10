struct preview{build(){Column() {
          // 搜索框
          Row() {
            // 搜索矢量图标设置高度和颜色
            Image($r("app.media.search")).height("3%").fillColor(Color.Gray)
              .padding({left: "40%"})
            TextInput({ placeholder: "搜索"}).backgroundColor(Color.Transparent)
              .padding({ left: 0 }) // 缩去和搜索图标的距离
              .defaultFocus(this.isSearchFocus)
              .focusOnTouch(true)
                // 确保当输入框获得焦点后，将isSearchFocus重置为false避免持续触发
              .onFocus(() => {
                this.isSearchFocus = false;
              })
          }
          .backgroundColor("#f4f6f5").borderRadius(20)
          .onClick(() => {
            console.log("1", this.isSearchFocus)
            this.isSearchFocus = true
            console.log("1", this.isSearchFocus)
          })
        }
        .padding({ left: 10, right: 10, bottom: 10})}}
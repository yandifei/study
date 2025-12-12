import { media } from '@kit.MediaKit'
import { common } from '@kit.AbilityKit';
import { BusinessError } from '@kit.BasicServicesKit'

const TAG: string = 'MediaDemo Audio#'

let player: media.AVPlayer;
// 异步创建播放器
media.createAVPlayer().then((audio: media.AVPlayer) => {
  if (audio != null) {
    player = audio;
    console.info('createAVPlayer success');
  } else {
    console.error('createAVPlayer fail');
  }
}).catch((error: BusinessError) => {
  console.error(`AVPlayer catchCallback, error message:${error.message}`);
});

@Entry
@Component
struct Index {
  @State hasInit: boolean = false;
  private context?: common.UIAbilityContext;
  stateChangeCallback: Function | undefined = undefined;

  aboutToAppear() {
    this.context = getContext(this) as common.UIAbilityContext
  }

  initAudioPlayer() {
    if(this.context){
      this.setCallback(player)
      this.context.resourceManager.getRawFd("music_wukong.mp3").then(value=>{
        player.fdSrc = value
      })
    }
  }
  setCallback(player: media.AVPlayer) {
    player.on('stateChange', this.stateChangeCallback = async (state: string, reason:
      media.StateChangeReason) => {
      switch (state) {
        case 'idle':
          console.info('state idle called');
          break;
        case 'initialized':
          console.info(TAG, 'initialized prepared called')
          this.hasInit = true;
          player.prepare().then(() => {
            player.play()
          })
          break;
        case 'playing':
          console.info(TAG, 'audio play success')
          break;
        case 'paused':
          console.info(TAG, 'audio paused success')
          break;
        case 'error':
          console.error('state error called');
          break;
        default:
          console.info('unkown state :' + state);
          break;
      }
    })
  }

  build() {
    Row() {
      Button({type: ButtonType.Circle, stateEffect: true}) {
        Image($r("app.media.play")).width(35).height(35)
      }
      .onClick(() => {
        console.info(TAG, "play button clicked, hasInit: " + this.hasInit)
        console.log("this.hasInit",this.hasInit)
        if (this.hasInit) {
          player.play()
        } else {
          this.initAudioPlayer()
        }
      })

      .id('btnAudioPlay')
      .backgroundColor(0xFFFFFF)
      .margin({right: 15})
      Button({type: ButtonType.Circle, stateEffect: true}) {
        Image($r("app.media.pause")).width(35).height(35)
      }
      .onClick(() => {
        player.pause()
      })
      .id('btnAudioStop')
      .backgroundColor(0xFFFFFF)
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
  }
}
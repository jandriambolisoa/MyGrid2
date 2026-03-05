import { Image, ImageProps } from "react-native"
//import * as Localization from "expo-localization"

export type StickerProps = ImageProps & {
  title?: 'DONE';
  size?: number;
  style?: any
}

export function Sticker ({
  title='DONE',
  size=50,
  style
}: StickerProps) {

  //const locale = Localization.getLocales()[0]?.languageCode || 'en'

  const stickers = {
    DONE: require('@/assets/images/stickers/done_v001.png')
  }

  return (
    <Image 
      source={stickers[title]}
      style={[{ 
        position: 'absolute',
        zIndex: 3,
        width: size,
        resizeMode: 'contain',
        transform: [
          { rotate: '60deg' }
        ]
      }, style]}
    />
  )
}
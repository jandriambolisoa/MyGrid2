import { randomNumber } from "@/utils";
import { Image, ImageProps } from "react-native";
import { useMemo } from "react";
import * as Localization from "expo-localization"

export type StickerProps = ImageProps & {
  title?: 'DONE';
  size?: number;
  randomizePosition?: boolean;
  randomizeRotation?: boolean;
  minTranslation?: number;
  maxTranslation?: number;
  minRotation?: number;
  maxRotation?: number;
  style?: any;
}

export function Sticker ({
  title='DONE',
  size=50,
  randomizePosition=true,
  randomizeRotation=true,
  minTranslation=-10,
  maxTranslation=10,
  minRotation=-60,
  maxRotation=60,
  style
}: StickerProps) {

  const locale = Localization.getLocales()[0]?.languageCode || 'en'

  const stickers = {
    DONE: locale === 'fr' ? require('@/assets/images/stickers/done_v001.fr.png') : require('@/assets/images/stickers/done_v001.en.png')
  }

  const transform = useMemo(() => [
    { rotate: randomizeRotation ? `${randomNumber(minRotation, maxRotation)}deg` : '0deg'},
    { translateX: randomizePosition ? randomNumber(minTranslation, maxTranslation) : 0},
    { translateY: randomizePosition ? randomNumber(minTranslation, maxTranslation) : 0}
  ], [randomizeRotation, randomizePosition, minTranslation, maxTranslation, minRotation, maxRotation])

  return (
    <Image 
      source={stickers[title]}
      style={[{ 
        position: 'absolute',
        zIndex: 3,
        width: size,
        resizeMode: 'contain',
        transform: transform
      }, style]}
    />
  )
}
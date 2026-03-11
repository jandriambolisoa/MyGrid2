import { Image, ImageProps } from 'react-native'
import { GlobalStyles } from '@/theme'

export type ProfilePictureProps = ImageProps & {
  borders?: boolean,
  link?: string | null,
  size?: number
}

export function ProfilePicture ({
  borders=false,
  link=null,
  size=50,
  style,
  ...otherProps
}: ProfilePictureProps) {

  const imageSource = link && link !== "" ? { uri: link } : require('@/assets/images/default/default_profile_picture_v001.png');

  return (
    <Image style={[GlobalStyles.profilePicture, {
      borderWidth: borders? 1 : 0,
      height: size,
      width: size
    }, style]} source={imageSource} {...otherProps}/>
  )
}
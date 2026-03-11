import { BackButton, Frame, FrameProps, MainText, SpotLight } from '@/components/widgets'
import { Constants, GlobalStyles } from '@/theme'
import { StyleSheet, View } from "react-native"

export type HeaderProps = FrameProps & {
  title?: string,
  subtitle?: string,
  subtitleColor?: string,
  backButton?: boolean,
  burgerMenu?: boolean,
  spotColor?: string | null
}

export function Header({
  title,
  subtitle,
  subtitleColor,
  backButton=true,
  burgerMenu=false,
  spotColor=null,
  ...otherProps
}: HeaderProps) {

  return (
    <Frame {...otherProps}>
      {spotColor && <View style={[StyleSheet.absoluteFill]}>
        <SpotLight color={spotColor} cx="40%" cy="40%" fx="10%" fy="10%" radius="70%"/>
      </View>}
      <View style={GlobalStyles.header}>
        {title && <MainText style={{ fontSize: Constants.fontSizes.header }} bold={true}>{title}</MainText>}
        {subtitle && <MainText style={[{ margin: 2 }, subtitleColor && { color: subtitleColor}]}>{subtitle}</MainText>}
        <BackButton />
      </View>
      {otherProps.children}
    </Frame>
  )
}
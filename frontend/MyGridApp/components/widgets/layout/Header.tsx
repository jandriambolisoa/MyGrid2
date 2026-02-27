import { BackButton, Frame, FrameProps, MainText } from '@/components/widgets'
import { Constants, GlobalStyles } from '@/theme'
import { View } from "react-native"

export type HeaderProps = FrameProps & {
  title?: string,
  subtitle?: string,
  backButton?: boolean,
  burgerMenu?: boolean
}

export function Header({
  title,
  subtitle,
  backButton=true,
  burgerMenu=false,
  ...otherProps
}: HeaderProps) {

  return (
    <Frame {...otherProps}>
      <View style={GlobalStyles.header}>
        {title && <MainText style={{ fontSize: Constants.fontSizes.header }} bold={true}>{title}</MainText>}
        {subtitle && <MainText style={{ margin: 2 }}>{subtitle}</MainText>}
        <BackButton />
      </View>
    </Frame>
  )
}
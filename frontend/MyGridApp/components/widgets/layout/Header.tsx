import { Frame, FrameProps, MainText } from '@/components/widgets'
import { Colors, Constants, GlobalStyles } from '@/theme'
import { Feather } from '@expo/vector-icons'
import { View, TouchableOpacity } from "react-native"
import { useRouter } from 'expo-router'

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

  const router = useRouter()

  return (
    <Frame {...otherProps}>
      <View style={GlobalStyles.header}>
        <MainText style={{ fontSize: Constants.fontSizes.header }} bold={true}>Prediction</MainText>
        <MainText >Make your prediction now</MainText>
        <TouchableOpacity
          style={{ position: 'absolute', width: 60, left: 0, bottom: 0, top: 0, alignItems: 'center', justifyContent: 'center' }}
          onPress={router.back}
        >
          <Feather name="arrow-left" size={36} color={Colors.light.lightText}/>
        </TouchableOpacity>
      </View>
    </Frame>
  )
}
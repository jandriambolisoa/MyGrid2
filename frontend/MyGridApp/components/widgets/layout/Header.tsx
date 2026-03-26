import { BackButton, Frame, FrameProps, MainText, SpotLight } from '@/components/widgets';
import { Constants, GlobalStyles, Colors } from '@/theme';
import { StyleSheet, TouchableOpacity, View, Platform } from "react-native";
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Feather } from '@expo/vector-icons';
import { useState } from 'react';
import { BlurView } from 'expo-blur';

type MenuItem = {
  title: string;
  onPress: () => void;
}

export type HeaderProps = FrameProps & {
  title?: string;
  subtitle?: string;
  subtitleColor?: string;
  backButton?: boolean;
  menu?: MenuItem[] | null;
  spotColor?: string | null
}

export function Header({
  title,
  subtitle,
  subtitleColor,
  backButton=true,
  menu=null,
  spotColor=null,
  ...otherProps
}: HeaderProps) {

  const insets = useSafeAreaInsets();

  const [showMenu, setShowMenu] = useState(false);

  const backgroundColor = Platform.OS === 'ios' ? 'transparent' : Colors.light.androidBackground

  return (
    <Frame {...otherProps}>
      {spotColor && <View style={[StyleSheet.absoluteFill]}>
        <SpotLight color={spotColor} cx="40%" cy="40%" fx="10%" fy="10%" radius="70%"/>
      </View>}
      <View style={GlobalStyles.header}>
        {title && <MainText style={{ fontSize: Constants.fontSizes.header }} bold={true}>{title}</MainText>}
        {subtitle && <MainText style={[{ margin: 2 }, subtitleColor && { color: subtitleColor}]}>{subtitle}</MainText>}
        {backButton && <BackButton />}
        {menu && <TouchableOpacity style={{
          position: 'absolute',
          width: Constants.spacing.backButtonSize,
          height: Constants.spacing.backButtonSize,
          right: 0,
          top: 0,
          alignItems: 'center',
          justifyContent: 'center'
        }}
        onPress={() => {setShowMenu(!showMenu)}}>
          <Feather name="menu" size={34} color={Colors.light.lightText}/>
        </TouchableOpacity>}
      </View>
      {otherProps.children}
      {menu && showMenu && <BlurView
        style={[GlobalStyles.button, {
          position: 'absolute',
          top: Constants.spacing.backButtonSize + insets.top,
          right: Constants.spacing.buttonMargin,
          minWidth: '50%',
          backgroundColor: backgroundColor
        }]}
        tint='light'
        intensity={20}
      >
        <SpotLight color={spotColor ?? undefined} cx="60%" cy="60%" fx="90%" fy="90%" radius="70%"/>
        <View style={{ padding: Constants.spacing.listMargin }}>
        {menu.map((item, index) => (
          <TouchableOpacity key={index} onPress={() => {item.onPress(); setShowMenu(false)}} style={{ height: Constants.spacing.wideMargin, justifyContent: 'center' }}>
            <MainText>{item.title}</MainText>
          </TouchableOpacity>
        ))}
        </View>
      </BlurView>}
    </Frame>
  )
}
import { TouchableOpacity, ViewProps, Animated, Platform } from "react-native";
import { Colors, Constants, GlobalStyles } from "@/theme";
import { MainText, MyGridBackground } from "@/components/widgets";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { BlurView } from "expo-blur";
import { useState, useEffect } from "react";
import { scopedI18n } from "@/translations/i18n";

export type PagerTabBarProps = ViewProps & {
  setPage?: (page: number) => void;
  scroll: Animated.Value;
  position: Animated.Value;
}

export function PagerTabBar ({
  setPage,
  scroll,
  position,
  ...otherProps
}: PagerTabBarProps) {

  const progress = Animated.add(position, scroll);
  const backgroundColor = Platform.OS === 'ios' ? 'transparent' : Colors.light.androidBackground;
  const paddingBottom = Platform.OS === 'ios' ? 0 : Constants.spacing.androidPadding;
  const hitSlop = 20; // For buttons to be easily clickable.
  const insets = useSafeAreaInsets();
  const t = scopedI18n('widgets.pagerTabBar');

  const [ firstTabDim, setFirstTabDim ] = useState<any>(null);
  const [ lastTabDim, setLastTabDim ] = useState<any>(null);
  const [ firstX, setFirstX ] = useState<number>(0);
  const [ lastX, setLastX ] = useState<number>(0);

  const left = progress?.interpolate({
    inputRange: [0, 1, 2],
    outputRange: [firstX, (firstX + lastX) / 2, lastX]
  });

  useEffect(() => {
    if (firstTabDim && lastTabDim) {
      setFirstX(firstTabDim.x + firstTabDim.width / 2);
      setLastX(lastTabDim.x + lastTabDim.width / 2);
    }
  }, [firstTabDim, lastTabDim]);

  return (
    <BlurView
      tint="light"
      intensity={20}
      style={[GlobalStyles.frame, GlobalStyles.tabBar, { paddingBottom: insets.bottom + paddingBottom + 6, backgroundColor: backgroundColor }]}
      {...otherProps}
    >
      {Platform.OS === 'android' && 
        <MyGridBackground/>
      }
      <TouchableOpacity onPress={() => setPage?.(0)} onLayout={(e) => setFirstTabDim(e.nativeEvent.layout)} hitSlop={hitSlop}>
        <MainText>{t('social')}</MainText>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => setPage?.(1)} hitSlop={hitSlop}>
        <MainText>{t('home')}</MainText>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => setPage?.(2)} onLayout={(e) => setLastTabDim(e.nativeEvent.layout)} hitSlop={hitSlop}>
        <MainText>{t('profile')}</MainText>
      </TouchableOpacity>
      <Animated.View style={[GlobalStyles.tabBarSlider, { bottom: insets.bottom + paddingBottom, left }]} />
    </BlurView>
  )
}
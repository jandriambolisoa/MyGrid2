import { TouchableOpacity, ViewProps, View } from "react-native";
import { GlobalStyles } from "@/theme";
import { MainText } from "@/components/widgets";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { BlurView } from "expo-blur";
import { useState, useEffect } from "react";
import { scopedI18n } from "@/translations/i18n";

export type PagerTabBarProps = ViewProps & {
  setPage?: (page: number) => void;
  scroll?: any;
}

export function PagerTabBar ({
  setPage,
  scroll,
  ...otherProps
}: PagerTabBarProps) {

  const insets = useSafeAreaInsets();

  const t = scopedI18n('widgets.pagerTabBar')

  const [ firstTabDim, setFirstTabDim ] = useState<any>(null);
  const [ lastTabDim, setLastTabDim ] = useState<any>(null);
  const [ firstX, setFirstX ] = useState<number>(0);
  const [ lastX, setLastX ] = useState<number>(0);

  useEffect(() => {
    if (firstTabDim && lastTabDim) {
      setFirstX(firstTabDim.x + firstTabDim.width / 2);
      setLastX(lastTabDim.x + lastTabDim.width / 2);
    }
  }, [firstTabDim, lastTabDim]);

  return (
    <BlurView tint="light" intensity={10} style={[GlobalStyles.frame, GlobalStyles.tabBar, { paddingBottom: insets.bottom }]} {...otherProps}>
      <TouchableOpacity onPress={() => setPage?.(0)} onLayout={(e) => setFirstTabDim(e.nativeEvent.layout)}>
        <MainText>{t('social')}</MainText>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => setPage?.(1)}>
        <MainText>{t('home')}</MainText>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => setPage?.(2)} onLayout={(e) => setLastTabDim(e.nativeEvent.layout)}>
        <MainText>{t('profile')}</MainText>
      </TouchableOpacity>
      <View style={[GlobalStyles.tabBarSlider, { bottom: insets.bottom - 6, left: (scroll?.offset + scroll?.position + .5) * (lastX - firstX) / 2 }]} />
    </BlurView>
  )
}
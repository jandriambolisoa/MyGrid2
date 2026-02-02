import { TouchableOpacity, ViewProps } from "react-native";
import { GlobalStyles } from "@/theme";
import { MainText } from "./MainText";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { BlurView } from "expo-blur";

export type PagerTabBarProps = ViewProps & {
  setPage?: (page: number) => void;
}

export function PagerTabBar ({
  setPage,
  ...otherProps
}: PagerTabBarProps) {

  const insets = useSafeAreaInsets();

  return (
    <BlurView tint="light" intensity={10} style={[GlobalStyles.tabBar, { paddingBottom: insets.bottom}]} {...otherProps}>
      <TouchableOpacity onPress={() => console.log("hello")}>
        <MainText>Social</MainText>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => console.log("hello")}>
        <MainText>Home</MainText>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => console.log("hello")}>
        <MainText>Profile</MainText>
      </TouchableOpacity>
    </BlurView>
  )
}
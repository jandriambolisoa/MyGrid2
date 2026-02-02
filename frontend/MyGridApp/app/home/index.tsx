import { useRef } from "react";
import PagerView from "react-native-pager-view";
import { View } from "react-native";
import { PagerTabBar } from "@/components/widgets";

import Events from "./events";
import Profile from "./profile";
import Social from "./social";

export default function HomePagerView () {

  const pagerRef = useRef<PagerView>(null);

  return (
    <View style= {{ flex: 1 }}>
      <PagerView
        ref={pagerRef}
        style={{ flex: 1 }}
        initialPage={1}
      >
        <Social />
        <Events />
        <Profile />
      </PagerView>
      <PagerTabBar />
    </View>
  )
}
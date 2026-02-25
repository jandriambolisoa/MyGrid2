import { useRef, useState } from "react";
import PagerView from "react-native-pager-view";
import { View } from "react-native";
import { PagerTabBar } from "@/components/widgets";
import { Colors } from "@/theme"

import Events from "./events";
import Profile from "./profile";
import Social from "./social";

export default function HomePagerView () {

  const pagerRef = useRef<PagerView>(null);
  
  const [scroll, setScroll] = useState<any>({ position: 1, offset: 0});
  const [tabBarHeight, setTabBarHeight] = useState(0);

  return (
    <View style= {{ flex: 1 }}>
      <PagerView
        ref={pagerRef}
        style={{ flex: 1, backgroundColor: Colors.light.background }}
        initialPage={1}
        overdrag={true}
        onPageScroll={(e) => {
          setScroll(e.nativeEvent);
        }}
      >
        <Social />
        <Events tabBarHeight={tabBarHeight}/>
        <Profile tabBarHeight={tabBarHeight}/>
      </PagerView>
      <PagerTabBar setPage={(page) => pagerRef.current?.setPage(page)} scroll={scroll} onLayout={(e) => setTabBarHeight(e.nativeEvent.layout.height)}/>
    </View>
  )
}
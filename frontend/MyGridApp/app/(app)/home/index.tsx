import { useRef, useState } from "react";
import PagerView from "react-native-pager-view";
import { View, Animated } from "react-native";
import { PagerTabBar } from "@/components/widgets";

import Events from "./events";
import Profile from "./profile";
import Social from "./social";

export default function HomePagerView () {

  const pagerRef = useRef<PagerView>(null);
  
  //const [scroll, setScroll] = useState<any>({ position: 1, offset: 0});
  const position = useRef(new Animated.Value(1)).current;
  const offset = useRef(new Animated.Value(0)).current;

  const [tabBarHeight, setTabBarHeight] = useState(0);

  return (
    <View style= {{ flex: 1 }}>
      <PagerView
        ref={pagerRef}
        style={{ flex: 1, backgroundColor: 'transparent' }}
        initialPage={1}
        overdrag={true}
        onPageScroll={Animated.event(
          [{ nativeEvent: { position, offset } }],
          { useNativeDriver: false }
        )}
      >
        <Social />
        <Events tabBarHeight={tabBarHeight}/>
        <Profile tabBarHeight={tabBarHeight}/>
      </PagerView>
      <PagerTabBar setPage={(page) => pagerRef.current?.setPage(page)} scroll={offset} position={position} onLayout={(e) => setTabBarHeight(e.nativeEvent.layout.height)}/>
    </View>
  )
}
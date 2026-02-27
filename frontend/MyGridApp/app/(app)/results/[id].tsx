import { Header, ScrollContainer } from "@/components/widgets";
import { useLocalSearchParams } from "expo-router";
import { View } from "react-native"
import { useState } from "react"

export default function Results () {

  const { id } = useLocalSearchParams();

  const [headerHeight, setHeaderHeight] = useState(0);
  const [footerHeight, setFooterHeight] = useState(0);

  return (
    <View style={{ flex: 1 }}>
      <ScrollContainer headerHeight={headerHeight}>
        <View style={{ backgroundColor: 'red', height: 100, width: 100 }}>

        </View>
      </ScrollContainer>
      <Header
        onLayout={(e: any) => setHeaderHeight(e.nativeEvent.layout.height)}
        title="Bahrain"
        subtitle="Le 25 février 2026"
      />
    </View>
  )
}
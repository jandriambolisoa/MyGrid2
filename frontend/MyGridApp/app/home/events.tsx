import { Container, MainWidget, ShadowButton } from "@/components/widgets";
import { Constants, GlobalStyles } from "@/theme";
import { Dimensions, ScrollView, Image } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export type EventsProps = {
  tabBarHeight?: number;
}

export default function Events ({ 
  tabBarHeight=0
}: EventsProps) {

  const insets = useSafeAreaInsets();
  const krunker = Image.resolveAssetSource(require('@/assets/images/demo/krunker.png'))

  return (
    <Container style={{ paddingBottom: 0 }}>
      <ScrollView style={{ alignSelf: 'stretch' }} contentContainerStyle={{ paddingBottom: tabBarHeight }}>
        <MainWidget style={{ height: Dimensions.get('window').height - insets.top - tabBarHeight - Constants.spacing.mainWidgetMargin}}/>
        <ShadowButton style={[GlobalStyles.mainWidget]}>
          <Image source={require('@/assets/images/demo/krunker.png')} style={{ height: 100, width: 500 }} resizeMode="stretch"/>
        </ShadowButton>
      </ScrollView>
    </Container>
  )
}
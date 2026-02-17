import { ViewProps, ScrollView } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Container }  from '@/components/widgets';

export type ScrollContainerProps = {
  tabBarHeight?: number;
} & ViewProps

// Scrollable container for home pages

export function ScrollContainer ({
  tabBarHeight=0,
  style,
  ...otherProps }: ScrollContainerProps ) {

  const insets = useSafeAreaInsets();

  return (
    <Container style={{ paddingBottom: 0, paddingTop: 0 }}>
      <ScrollView style={{ alignSelf: 'stretch' }} contentContainerStyle={{ paddingBottom: tabBarHeight, paddingTop: insets.top }} showsVerticalScrollIndicator={false}>
        {otherProps.children}
      </ScrollView>
    </Container>
  )
}
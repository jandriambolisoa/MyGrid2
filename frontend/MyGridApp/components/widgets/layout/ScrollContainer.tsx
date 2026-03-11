import { ScrollView, ScrollViewProps } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Container }  from '@/components/widgets';

export type ScrollContainerProps = {
  footerHeight?: number;
  headerHeight?: number;
} & ScrollViewProps

// Scrollable container for home pages

export function ScrollContainer ({
  footerHeight=0,
  headerHeight=0,
  style,
  ...otherProps }: ScrollContainerProps ) {

  const insets = useSafeAreaInsets();
  const paddingBottom = footerHeight ? footerHeight : insets.bottom
  const paddingTop = headerHeight ? headerHeight : insets.top

  return (
    <Container style={{ paddingBottom: 0, paddingTop: 0 }}>
      <ScrollView
        style={{ alignSelf: 'stretch' }}
        contentContainerStyle={{ paddingBottom: paddingBottom, paddingTop: paddingTop }}
        showsVerticalScrollIndicator={false}
        {...otherProps}
      >
        {otherProps.children}
      </ScrollView>
    </Container>
  )
}
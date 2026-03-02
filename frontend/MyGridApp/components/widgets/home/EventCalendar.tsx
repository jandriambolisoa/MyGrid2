import { Colors, Constants, GlobalStyles } from "@/theme"
import { TouchableOpacityProps, TouchableOpacity, Dimensions, FlatList, View, Animated, Image, StyleSheet } from "react-native"
import { MainText, Shadow, ShadowSetup, SpotLight } from "@/components/widgets"
import { DateTime } from "luxon"
import { useRef, useEffect, useState } from "react"
import { fromToDatetime } from "@/utils"
import { scopedI18n } from "@/translations/i18n"

const t = scopedI18n('widgets.eventCalendar')

export type EventCalendarWidgetProps = {
  size?: number,
  scroll?: Animated.Value,
  datas?: any,
  index?: number
} & TouchableOpacityProps

export function EventCalendarWidget ({
  size=0,
  scroll= new Animated.Value(0),
  datas=null,
  index=0,
  ...otherProps
}: EventCalendarWidgetProps) {

  const inputRange = [
    (index - 1) * (size + Constants.spacing.buttonPadding),
    index * (size + Constants.spacing.buttonPadding),
    (index + 1) * (size + Constants.spacing.buttonPadding),
  ];

  const scale = scroll.interpolate({ 
    inputRange,
    outputRange: [0.8, 1, 0.8],
    extrapolate: 'clamp'
  })

  // Temporary disable -> should be removed after event page creation
  const disabled = true;

  const [showShadow, setShowShadow] = useState(true);

  useEffect(() => {
    // Add listener to scroll Animated.Value
    const id = scroll.addListener(({ value }) => {
      const itemCenter = index * (size + Constants.spacing.buttonPadding);
      // Show shadow only if scroll is "close" to this item
      if (value < itemCenter - size * 2 || value > itemCenter + size * 2) {
        setShowShadow(false);
      } else {
        setShowShadow(true);
      }
    });

    return () => scroll.removeListener(id);
  }, [scroll, index, size]);

  return(
    <TouchableOpacity style={[GlobalStyles.button, { height: size, width: size, alignSelf: 'center', transform: [{ scale: scale }]  }]} disabled={disabled}>
      {showShadow && 
        <>
          <SpotLight color={datas?.colors[0] || Colors.light.background} cx="35%" cy="35%" fx="5%" fy="5%" radius="50%"/>
          <ShadowSetup />
        </>
      }
      <MainText>{datas?.name}</MainText>
      <Image source={{ uri: datas?.flag }} style={{ height: 50, width: 80, margin: Constants.spacing.buttonPadding }} resizeMode="cover"/>
      <MainText>{fromToDatetime(datas?.datetime)}</MainText>
    </TouchableOpacity>
  )
}

export type EventCalendarProps = {
  datas?: any
}

export function EventCalendar ({
  datas = null
}: EventCalendarProps) {

  // Function to sort events by date (may be removed later)
  function compareDates(a: any, b: any) {
    return DateTime.fromISO(a.datetime).toMillis() - DateTime.fromISO(b.datetime).toMillis()
  }
  
  const sortedDatas = datas ? datas.events.sort(compareDates) : [];

  const windowWidth = Dimensions.get('window').width;
  const size = windowWidth * 0.65;
  const blankSpace = (windowWidth - size) / 2;
  const index = sortedDatas.findIndex((item: any) => DateTime.fromISO(item.datetime) > DateTime.now()) || sortedDatas.length - 1;
  const firstPage = index === -1 ? sortedDatas.length - 1 : index;
  const initialScrollX = firstPage * (size + Constants.spacing.buttonPadding);
  const scrollX = useRef(new Animated.Value(initialScrollX)).current;

  return (
    <View>
      <MainText bold={true} style={{ fontSize: 20, alignSelf: 'center', marginBottom: Constants.spacing.buttonPadding }}>
        {t('calendar')}
      </MainText>
      <FlatList
        data={sortedDatas}
        horizontal={true}
        snapToInterval={size + Constants.spacing.buttonPadding}
        decelerationRate="fast"
        showsHorizontalScrollIndicator={false}
        style={{ paddingBottom: Constants.spacing.mainWidgetMargin, alignSelf: 'stretch' }}
        contentContainerStyle={{ paddingHorizontal: blankSpace }}
        ItemSeparatorComponent={() => <View style={{ width: Constants.spacing.buttonPadding }}/>}
        contentOffset={{ x: initialScrollX, y: 0 }}
        onScroll={Animated.event(
          [{ nativeEvent: { contentOffset: { x: scrollX } } }],
          { useNativeDriver: false }
        )}
        renderItem={({ item, index }) => (
          <EventCalendarWidget size={size} scroll={scrollX} datas={item} index={index}/>
        )}
      />
      <View style={StyleSheet.absoluteFill} pointerEvents="none">
        <Shadow orientation="left" color={Colors.light.background} opacityStart="1"/>
        <Shadow orientation="right" color={Colors.light.background} opacityStart="1"/>
      </View>
    </View>
  )
}
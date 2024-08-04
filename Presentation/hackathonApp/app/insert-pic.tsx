import {
  View,
  Text,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  TextInput,
} from "react-native";
import { AntDesign } from "@expo/vector-icons";
import React, { useState } from "react";
import * as ImagePicker from "expo-image-picker";
import { Link } from "expo-router";

import ImageViewer from "../components/imageViewer";

const PlaceholderImage = require("@/assets/images/gradient.png");

const InsertPic = () => {
  const [inputText, setInputText] = useState("");
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [icon, setIcon] = useState<"plus" | "close">("plus");

  const pickImageAsync = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      allowsEditing: true,
      quality: 1,
    });

    if (!result.canceled) {
      setSelectedImage(result.assets[0].uri);
    } else {
      alert("You did not select any image");
    }
  };

  const handleImage = () => {
    if (selectedImage) {
      setSelectedImage(null);
      setIcon("plus");
    } else {
      pickImageAsync();
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      keyboardVerticalOffset={80}
      style={styles.container}
    >
      <View style={{ alignSelf: "center" }}>
        <Pressable style={{ alignItems: "center" }} onPress={handleImage}>
          <ImageViewer
            placeholderImage={PlaceholderImage}
            selectedImage={selectedImage}
          />
          <AntDesign name={icon} size={24} color={"#314053"} />
        </Pressable>
      </View>

      <View style={{ gap: 5, flex: 1 }}>
        <Text style={{ fontSize: 24, paddingLeft: 5 }}>Add a question</Text>
        <TextInput
          placeholder="Add some information..."
          placeholderTextColor={"#314053"}
          onChangeText={(text) => setInputText(text)}
          value={inputText}
          style={styles.input}
        />
      </View>
      <Link
        href={{
          pathname: "/result/",
          params: { input: inputText },
        }}
        asChild
      >
        <Pressable style={styles.search}>
          <Text style={styles.searchText}>SEARCH</Text>
        </Pressable>
      </Link>
    </KeyboardAvoidingView>
  );
};

export default InsertPic;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingVertical: 60,
    paddingHorizontal: 15,
    gap: 80,
  },
  arrow: {
    padding: 10,
    borderRadius: 15,
    backgroundColor: "#E1E8EE",
    justifyContent: "center",
    alignItems: "center",
  },
  search: {
    height: 50,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#314053",
    borderRadius: 12,
    marginBottom: 30,
  },
  searchText: {
    color: "white",
    fontSize: 24,
    fontFamily: "niv-r-smallcaps",
  },
  input: {
    height: 50,
    paddingHorizontal: 10,
    backgroundColor: "#E1E8EE",
    borderRadius: 12,
    fontSize: 18,
    fontFamily: "niv-r-smallcaps",
  },
});

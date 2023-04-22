using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using NativeWebSocket;
using System;

public class ESP32 : MonoBehaviour
{
    private WebSocket _webSocket;
    public Plane p;

    // Start is called before the first frame update
    async void Start()
    {
        p.Flip();
        _webSocket = new WebSocket("ws://192.168.137.1:8888");
        _webSocket.OnOpen += () => { print("Connection Open!"); };
        _webSocket.OnError += (e) => { print("Error :" + e); };
        _webSocket.OnClose += (e) => { print("Connection Close!"); };
        _webSocket.OnMessage += (bytes) =>
        {
            print("onMessage length :" + bytes.Length);
            if (bytes.Length > 0)
            {
                Texture2D tex = new Texture2D(2, 2);
                tex.LoadImage(bytes);

                // var pix = tex.GetPixels32();
                // Array.Reverse(pix);
                //
                // var destTex = new Texture2D(tex.width, tex.height);
                // destTex.SetPixels32(pix);
                // destTex.Apply();

                if (GetComponent<Renderer>() != null)
                {
                    GetComponent<Renderer>().material.mainTexture = tex;
                }
            }
        };
        await _webSocket.Connect();
    }

    // Update is called once per frame
    void Update()
    {
        _webSocket.DispatchMessageQueue();
    }

    private async void OnApplicationQuit()
    {
        await _webSocket.Close();
    }
}

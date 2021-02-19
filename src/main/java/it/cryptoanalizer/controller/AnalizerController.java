package it.cryptoanalizer.controller;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
public class AnalizerController {

    @RequestMapping(value = "/update", method = RequestMethod.POST)
    public String updateData(final @RequestBody String body){
        System.out.println(body);
        return "json test";



    }
}

import { Component, OnInit, Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import {DetectorService} from './detector.service';
import {  FormBuilder, FormGroup, Validators  } from '@angular/forms';
import { NgxSpinnerService } from "ngx-spinner";

@Component({
  selector: 'app-detector',
  templateUrl: './detector.component.html',
  styleUrls: ['./detector.component.css'],
  providers:[DetectorService]
})
export class DetectorComponent implements OnInit {
  resultValue : any; 
  flairDetectorform: FormGroup;
  constructor(private formBuilder: FormBuilder,private service:DetectorService,
    private spinner: NgxSpinnerService,private http : HttpClient) { }

  ngOnInit() {
    this.formInitialize();
  }
  formInitialize () {
    this.flairDetectorform = this.formBuilder.group({
      inputURL: ['',[Validators.required]]
    });
  }
  onSubmit(): void{
    this.spinner.show();
    const url = this.flairDetectorform.get('inputURL').value;
    const urlFromUI = {"url":url};
    this.http.post('https://flair-detection-backend.herokuapp.com/api/getflair',urlFromUI).subscribe(data => {
      this.spinner.hide();
      this.resultValue = data[url];
    })
  }
  

}

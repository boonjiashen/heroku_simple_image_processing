#!/usr/bin/env node
import * as cdk from 'monocdk';
import { HerokuSimpleImageProcessingStack } from '../lib/heroku_simple_image_processing-stack';

const app = new cdk.App();
new HerokuSimpleImageProcessingStack(app, 'HerokuSimpleImageProcessingStack');
